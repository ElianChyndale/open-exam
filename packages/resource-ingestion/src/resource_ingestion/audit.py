from __future__ import annotations

from hashlib import sha256
from typing import Any

from resource_ingestion.models import AuditFinding
from resource_ingestion.policy import LICENSE_MODES


def _finding(check_id: str, severity: str, evidence: list[str], remediation: str) -> dict[str, Any]:
    finding_id = "finding-" + sha256("|".join([check_id, *evidence]).encode("utf-8")).hexdigest()[:16]
    return AuditFinding(
        finding_id=finding_id,
        scope="content",
        check_id=check_id,
        severity=severity,
        evidence=evidence,
        remediation=remediation,
    ).as_dict()


def audit_documents(documents: list[dict[str, Any]]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for document in documents:
        evidence = [document["document_id"], document["url"]]
        if document.get("license_mode") not in LICENSE_MODES:
            findings.append(_finding("resource.license.invalid", "high", evidence, "Quarantine the resource and record an explicit license policy."))
        if document.get("license_mode") == "metadata_only" and document.get("content_ref"):
            findings.append(_finding("resource.metadata_only.fulltext_retained", "high", evidence, "Purge retained full text and rebuild the private index."))
        if not document.get("content_hash"):
            findings.append(_finding("resource.hash.missing", "high", evidence, "Re-ingest the resource to create a content hash."))
    return findings
