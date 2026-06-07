'use client';

import Link from 'next/link';

export function AssistantActionCard({ action }: { action: any }) {
  return (
    <div className="mt-2 rounded-lg border border-line bg-surface-field p-3 text-xs">
      <p className="font-semibold">{action.summary || action.action_type}</p>
      {action.launch_route ? (
        <Link href={action.launch_route} className="mt-2 inline-block font-semibold text-accent hover:underline">
          Open route
        </Link>
      ) : null}
      {action.card_id ? <p className="mt-1 text-muted">Card: {action.card_id}</p> : null}
      {action.attempt_id ? <p className="mt-1 text-muted">Attempt: {action.attempt_id}</p> : null}
    </div>
  );
}
