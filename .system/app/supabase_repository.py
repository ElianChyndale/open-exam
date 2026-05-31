"""Optional Supabase bridge with explicit transfer only."""

from __future__ import annotations

import json
import os
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from app.storage import LocalRepository


class SupabaseRepository(LocalRepository):
    """Local working repository plus explicit tenant-safe cloud transfer.

    Event writes remain local until a caller requests a transfer. This avoids
    accidental bidirectional sync and keeps the CLI usable during outages.
    """

    def __init__(self, root) -> None:
        self.supabase_url = os.getenv("SUPABASE_URL", "").rstrip("/")
        self.publishable_key = os.getenv("SUPABASE_PUBLISHABLE_KEY", "")
        self.service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
        if not self.supabase_url or not self.publishable_key:
            raise ValueError("SUPABASE_URL and SUPABASE_PUBLISHABLE_KEY are required in supabase mode")
        super().__init__(root)

    def push_bundle(self, bundle: dict, organization_id: str, *, dry_run: bool = True) -> dict:
        streams = bundle.get("streams", {})
        events = [
            {
                "organization_id": organization_id,
                "learner_id": event.get("learner_id", "local"),
                "stream": stream,
                "event_id": event["event_id"],
                "event_type": event["event_type"],
                "schema_version": event.get("schema_version", 1),
                "occurred_at": event["occurred_at"],
                "source_refs": event.get("source_refs", []),
                "payload": event.get("payload", {}),
            }
            for stream, stream_events in streams.items()
            for event in stream_events
        ]
        summary = {
            "direction": "local-to-cloud",
            "dry_run": dry_run,
            "organization_id": organization_id,
            "event_count": len(events),
        }
        if dry_run:
            return summary
        if not organization_id:
            raise ValueError("organization_id is required for cloud transfer")
        if not self.service_role_key:
            raise ValueError("SUPABASE_SERVICE_ROLE_KEY is required for committed cloud transfer")
        self._postgrest_insert("learning_events", events)
        return {**summary, "uploaded_event_count": len(events)}

    def _postgrest_insert(self, table: str, rows: list[dict]) -> None:
        if not rows:
            return
        request = Request(
            f"{self.supabase_url}/rest/v1/{table}",
            data=json.dumps(rows).encode("utf-8"),
            method="POST",
            headers={
                "apikey": self.service_role_key,
                "Authorization": f"Bearer {self.service_role_key}",
                "Content-Type": "application/json",
                "Prefer": "resolution=merge-duplicates",
            },
        )
        try:
            with urlopen(request, timeout=30):
                pass
        except HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Supabase transfer failed: {error.code} {detail}") from error
