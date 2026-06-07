'use client';

import React from 'react';

interface ReviewProjectionProps {
  markdown: string;
}

type Section =
  | { type: 'heading'; level: 1 | 2 | 3 | 4; text: string }
  | { type: 'paragraph'; text: string }
  | { type: 'list'; items: string[] }
  | { type: 'blockquote'; lines: string[] }
  | { type: 'callout'; kind: string; title: string; lines: string[]; collapsed: boolean };

interface ParsedProjection {
  frontmatter: Record<string, string>;
  sections: Section[];
}

export function ReviewProjection({ markdown }: ReviewProjectionProps) {
  const parsed = React.useMemo(() => parseProjection(markdown), [markdown]);

  return (
    <div className="space-y-5">
      {Object.keys(parsed.frontmatter).length > 0 && (
        <section className="rounded-lg border border-line bg-surface-raised p-4">
          <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
            {Object.entries(parsed.frontmatter).map(([key, value]) => (
              <div key={key} className="rounded-lg bg-surface-field p-3">
                <p className="text-[11px] uppercase tracking-wide text-muted">{humanizeKey(key)}</p>
                <p className="mt-1 text-sm font-semibold">{value}</p>
              </div>
            ))}
          </div>
        </section>
      )}

      <article className="rounded-lg border border-line bg-surface-raised p-5">
        <div className="space-y-4">
          {parsed.sections.map((section, index) => (
            <SectionView key={`${section.type}-${index}`} section={section} />
          ))}
        </div>
      </article>
    </div>
  );
}

function SectionView({ section }: { section: Section }) {
  if (section.type === 'heading') {
    if (section.level === 1) return <h1 className="text-2xl font-bold">{section.text}</h1>;
    if (section.level === 2) return <h2 className="pt-2 text-xl font-semibold">{section.text}</h2>;
    if (section.level === 3) return <h3 className="text-lg font-semibold">{section.text}</h3>;
    return <h4 className="text-sm font-semibold uppercase tracking-wide text-muted">{section.text}</h4>;
  }

  if (section.type === 'paragraph') {
    return <p className="text-sm leading-7 text-ink">{renderInline(section.text)}</p>;
  }

  if (section.type === 'list') {
    return (
      <ul className="space-y-2 pl-5 text-sm leading-7 text-ink">
        {section.items.map((item, index) => (
          <li key={index} className="list-disc">
            {renderInline(item)}
          </li>
        ))}
      </ul>
    );
  }

  if (section.type === 'blockquote') {
    return (
      <blockquote className="border-l-4 border-accent-soft bg-surface-field px-4 py-3 text-sm leading-7 text-ink">
        {section.lines.map((line, index) => (
          <p key={index}>{renderInline(line)}</p>
        ))}
      </blockquote>
    );
  }

  const title = section.title || humanizeKey(section.kind);
  const collapseByDefault = section.collapsed || section.kind.toLowerCase() === 'answer';

  if (collapseByDefault) {
    return (
      <details className="overflow-hidden rounded-lg border border-accent-soft bg-surface-field">
        <summary className="cursor-pointer list-none border-b border-accent-soft bg-accent-soft px-4 py-2 text-sm font-semibold text-accent">
          {title}
        </summary>
        <div className="space-y-3 px-4 py-3 text-sm leading-7 text-ink">
          <CalloutLinesView lines={section.lines} />
        </div>
      </details>
    );
  }

  return (
    <div className="overflow-hidden rounded-lg border border-accent-soft bg-surface-field">
      <div className="border-b border-accent-soft bg-accent-soft px-4 py-2 text-sm font-semibold text-accent">
        {title}
      </div>
      <div className="space-y-3 px-4 py-3 text-sm leading-7 text-ink">
        <CalloutLinesView lines={section.lines} />
      </div>
    </div>
  );
}

function CalloutLinesView({ lines }: { lines: string[] }) {
  const blocks: Array<
    | { type: 'heading'; text: string }
    | { type: 'list'; items: string[] }
    | { type: 'paragraph'; text: string }
  > = [];

  let index = 0;
  while (index < lines.length) {
    const trimmed = lines[index].trim();
    if (!trimmed) {
      index += 1;
      continue;
    }

    if (trimmed.startsWith('#### ')) {
      blocks.push({ type: 'heading', text: trimmed.slice(5) });
      index += 1;
      continue;
    }

    if (trimmed.startsWith('- ')) {
      const items: string[] = [];
      while (index < lines.length && lines[index].trim().startsWith('- ')) {
        items.push(lines[index].trim().slice(2));
        index += 1;
      }
      blocks.push({ type: 'list', items });
      continue;
    }

    const paragraph: string[] = [trimmed];
    index += 1;
    while (index < lines.length) {
      const next = lines[index].trim();
      if (!next || next.startsWith('#### ') || next.startsWith('- ')) break;
      paragraph.push(next);
      index += 1;
    }
    blocks.push({ type: 'paragraph', text: paragraph.join(' ') });
  }

  return (
    <>
      {blocks.map((block, index) => {
        if (block.type === 'heading') {
          return <h4 key={index} className="text-[11px] font-semibold uppercase tracking-wide text-muted">{block.text}</h4>;
        }
        if (block.type === 'list') {
          return (
            <ul key={index} className="space-y-2 pl-5">
              {block.items.map((item, itemIndex) => (
                <li key={itemIndex} className="list-disc">
                  {renderInline(item)}
                </li>
              ))}
            </ul>
          );
        }
        return <p key={index}>{renderInline(block.text)}</p>;
      })}
    </>
  );
}

function parseProjection(markdown: string): ParsedProjection {
  const lines = markdown.replace(/\r\n/g, '\n').split('\n');
  const frontmatter: Record<string, string> = {};
  let index = 0;

  if (lines[0] === '---') {
    index = 1;
    for (; index < lines.length; index += 1) {
      const line = lines[index];
      if (line === '---') {
        index += 1;
        break;
      }
      const colon = line.indexOf(':');
      if (colon > 0) {
        frontmatter[line.slice(0, colon).trim()] = line.slice(colon + 1).trim();
      }
    }
  }

  const sections: Section[] = [];

  while (index < lines.length) {
    const raw = lines[index];
    const line = raw.trimEnd();
    const trimmed = line.trim();

    if (!trimmed) {
      index += 1;
      continue;
    }

    if (trimmed.startsWith('#### ')) {
      sections.push({ type: 'heading', level: 4, text: trimmed.slice(5) });
      index += 1;
      continue;
    }
    if (trimmed.startsWith('### ')) {
      sections.push({ type: 'heading', level: 3, text: trimmed.slice(4) });
      index += 1;
      continue;
    }
    if (trimmed.startsWith('## ')) {
      sections.push({ type: 'heading', level: 2, text: trimmed.slice(3) });
      index += 1;
      continue;
    }
    if (trimmed.startsWith('# ')) {
      sections.push({ type: 'heading', level: 1, text: trimmed.slice(2) });
      index += 1;
      continue;
    }

    if (trimmed.startsWith('> [!')) {
      const match = trimmed.match(/^>\s*\[!([^\]]+)\]([+-]?)\s*(.*)$/);
      const kind = match?.[1] || 'note';
      const collapsed = match?.[2] === '-';
      const title = match?.[3] || '';
      const calloutLines: string[] = [];
      index += 1;
      while (index < lines.length && lines[index].trimStart().startsWith('>')) {
        calloutLines.push(lines[index].replace(/^\s*>\s?/, '').trimEnd());
        index += 1;
      }
      sections.push({
        type: 'callout',
        kind,
        title,
        collapsed,
        lines: calloutLines.filter((entry) => entry.trim().length > 0),
      });
      continue;
    }

    if (trimmed.startsWith('>')) {
      const quoteLines: string[] = [];
      while (index < lines.length && lines[index].trimStart().startsWith('>')) {
        quoteLines.push(lines[index].replace(/^\s*>\s?/, '').trimEnd());
        index += 1;
      }
      sections.push({ type: 'blockquote', lines: quoteLines.filter((entry) => entry.trim().length > 0) });
      continue;
    }

    if (trimmed.startsWith('- ')) {
      const items: string[] = [];
      while (index < lines.length) {
        const next = lines[index].trim();
        if (next.startsWith('- ')) {
          items.push(next.slice(2));
          index += 1;
          continue;
        }
        break;
      }
      sections.push({ type: 'list', items });
      continue;
    }

    const paragraph: string[] = [trimmed];
    index += 1;
    while (index < lines.length) {
      const next = lines[index].trim();
      if (!next || next.startsWith('#') || next.startsWith('- ') || next.startsWith('>')) break;
      paragraph.push(next);
      index += 1;
    }
    sections.push({ type: 'paragraph', text: paragraph.join(' ') });
  }

  return { frontmatter, sections };
}

function renderInline(text: string): React.ReactNode {
  const parts: Array<{ type: 'text' | 'bold' | 'code'; value: string }> = [];
  let remaining = text;

  while (remaining.length > 0) {
    const codeMatch = remaining.match(/`([^`]+)`/);
    const boldMatch = remaining.match(/\*\*([^*]+)\*\*/);
    const candidates = [codeMatch, boldMatch].filter(Boolean) as RegExpMatchArray[];
    if (candidates.length === 0) {
      parts.push({ type: 'text', value: remaining });
      break;
    }
    const next = candidates.sort((a, b) => (a.index ?? 0) - (b.index ?? 0))[0];
    const start = next.index ?? 0;
    if (start > 0) {
      parts.push({ type: 'text', value: remaining.slice(0, start) });
    }
    const token = next[0];
    const value = next[1];
    parts.push({ type: token.startsWith('`') ? 'code' : 'bold', value });
    remaining = remaining.slice(start + token.length);
  }

  return (
    <>
      {parts.map((part, index) => {
        if (part.type === 'bold') return <strong key={index}>{part.value}</strong>;
        if (part.type === 'code') return <code key={index} className="rounded bg-surface-canvas px-1 py-0.5 text-[0.95em]">{part.value}</code>;
        return <React.Fragment key={index}>{part.value}</React.Fragment>;
      })}
    </>
  );
}

function humanizeKey(value: string) {
  return value.replace(/[_-]+/g, ' ').replace(/\b\w/g, (letter) => letter.toUpperCase());
}
