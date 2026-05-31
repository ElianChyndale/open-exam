'use client';

import { useEffect, useState } from 'react';
import { BookOpen, ChevronDown, Library, Target } from 'lucide-react';
import Link from 'next/link';
import { curriculumApi } from '@/lib/api';
import { Badge, EmptyState, Surface } from '@/components/ui/ui';

export default function CurriculumMapPage() {
  const [data, setData] = useState<{ subject_count: number; module_count: number; subjects: any[] } | null>(null);

  useEffect(() => { curriculumApi.get().then(setData); }, []);

  return (
    <div className="mx-auto max-w-6xl space-y-5">
      <header className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <p className="metric-label">Official 2026 registry</p>
          <h1 className="mt-1 text-3xl font-semibold tracking-tight">Curriculum map</h1>
          <p className="mt-2 text-sm text-muted">Navigate from topic weights to modules and LOS without losing the evidence trail.</p>
        </div>
        <div className="flex items-center gap-2"><Link className="button-secondary" href="/graph">Open graph</Link><Badge tone="accent">{data?.subject_count ?? '...'} subjects</Badge><Badge>{data?.module_count ?? '...'} modules</Badge></div>
      </header>
      {!data ? <Surface className="animate-pulse text-sm text-muted">Loading official curriculum...</Surface> : null}
      {data?.subjects.length === 0 ? <EmptyState title="No curriculum registry found" /> : null}
      <div className="grid gap-3 md:grid-cols-2">
        {data?.subjects.map((subject) => (
          <Surface key={subject.subject} className="space-y-3">
            <div className="flex items-start justify-between gap-3">
              <div><h2 className="font-semibold tracking-tight">{subject.subject}</h2><p className="mt-1 text-xs text-muted">{subject.module_count} modules</p></div>
              <Badge tone="accent">{subject.exam_weight}</Badge>
            </div>
            <div className="space-y-2">
              {subject.modules.map((module: any) => (
                <details key={module.module} className="rounded-xl border border-line/80 bg-surface-raised/60 px-3 py-2">
                  <summary className="flex cursor-pointer list-none items-center gap-2 text-sm font-medium">
                    <ChevronDown size={14} className="text-muted" /><span>{module.module}</span><span className="truncate text-muted">{module.official_module}</span>
                  </summary>
                  <ul className="mt-2 space-y-1 border-t border-line/70 pt-2">
                    {module.los.map((los: string) => <li key={los} className="flex gap-2 text-xs text-muted"><Target size={12} className="mt-0.5 shrink-0 text-accent" />{los}</li>)}
                  </ul>
                </details>
              ))}
            </div>
          </Surface>
        ))}
      </div>
    </div>
  );
}
