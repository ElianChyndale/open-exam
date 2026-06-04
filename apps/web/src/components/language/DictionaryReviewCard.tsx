import type { DictionaryResult } from '@/lib/api';

import {
  SpanishConjugationTable,
  type DictionaryEntryLike,
  type DictionarySenseLike,
  isSpanishVerbItem,
} from '@/components/language/SpanishConjugationTable';

function isDictionaryResult(value: DictionaryResult | DictionaryEntryLike): value is DictionaryResult {
  return 'entry_json' in value;
}

function safeParseEntryJson(raw: string): DictionaryEntryLike | null {
  try {
    return JSON.parse(raw) as DictionaryEntryLike;
  } catch {
    return null;
  }
}

export function normalizeDictionaryEntry(item: DictionaryResult | DictionaryEntryLike): DictionaryEntryLike {
  if (!isDictionaryResult(item)) {
    return item;
  }

  const parsed = safeParseEntryJson(item.entry_json);
  if (parsed) {
    return parsed;
  }

  return {
    lemma: item.lemma,
    pos: item.pos,
    language: item.language,
    source_id: item.source_id,
    senses: item.definition
      ? [
          {
            definition: item.definition,
          },
        ]
      : [],
  };
}

export function collectCefrLevels(entry: DictionaryEntryLike): string[] {
  const levels = new Set<string>();
  for (const sense of entry.senses ?? []) {
    if (sense.cefr_level?.trim()) {
      levels.add(sense.cefr_level.trim().toUpperCase());
    }
  }
  return [...levels];
}

function collectTranslations(item: DictionaryResult | DictionaryEntryLike, entry: DictionaryEntryLike): string[] {
  const translations = new Set<string>();

  if (isDictionaryResult(item) && item.translation?.trim()) {
    item.translation
      .split(/[,;/]/)
      .map((value) => value.trim())
      .filter(Boolean)
      .forEach((value) => translations.add(value));
  }

  for (const sense of entry.senses ?? []) {
    for (const mapping of sense.translations ?? []) {
      if (mapping?.target_lemma?.trim()) {
        translations.add(mapping.target_lemma.trim());
      }
    }
  }

  return [...translations];
}

function primarySense(entry: DictionaryEntryLike, item: DictionaryResult | DictionaryEntryLike): DictionarySenseLike | null {
  if (entry.senses?.length) {
    return entry.senses[0] ?? null;
  }
  if (isDictionaryResult(item) && item.definition?.trim()) {
    return { definition: item.definition.trim() };
  }
  return null;
}

function badge(label: string, value: string, tone: 'default' | 'accent' = 'default') {
  const toneClass =
    tone === 'accent'
      ? 'border-accent/30 bg-accent/10 text-accent'
      : 'border-line bg-surface-raised text-muted';
  return (
    <span className={`rounded-full border px-2 py-1 text-[10px] font-medium uppercase tracking-wide ${toneClass}`}>
      {label ? `${label}: ${value}` : value}
    </span>
  );
}

export function DictionaryReviewCard({
  item,
  showConjugation = true,
}: {
  item: DictionaryResult | DictionaryEntryLike;
  showConjugation?: boolean;
}) {
  const entry = normalizeDictionaryEntry(item);
  const mainSense = primarySense(entry, item);
  const cefrLevels = collectCefrLevels(entry);
  const translations = collectTranslations(item, entry);
  const examples = (mainSense?.examples ?? []).filter(Boolean);
  const additionalSenses = (entry.senses ?? []).slice(1, 4).filter((sense) => sense.definition?.trim());
  const synonyms = (mainSense?.synonyms ?? []).filter(Boolean).slice(0, 5);
  const antonyms = (mainSense?.antonyms ?? []).filter(Boolean).slice(0, 3);

  return (
    <article className="space-y-4 rounded-2xl border border-line bg-surface p-4">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div className="space-y-2">
          <div className="flex flex-wrap items-center gap-2">
            <h3 className="text-lg font-semibold text-ink">{entry.lemma || (isDictionaryResult(item) ? item.lemma : 'Unknown lemma')}</h3>
            {entry.pos ? badge('', entry.pos) : null}
            {entry.language ? badge('', entry.language) : null}
            {entry.gender ? badge('gender', entry.gender) : null}
            {cefrLevels.map((level) => (
              <span key={level}>{badge('CEFR', level, 'accent')}</span>
            ))}
          </div>
          {entry.pronunciation ? (
            <p className="text-sm text-muted">Pronunciation: {entry.pronunciation}</p>
          ) : null}
        </div>
        {translations.length ? (
          <div className="max-w-sm text-right">
            <div className="text-[10px] uppercase tracking-wide text-muted">Translations</div>
            <div className="mt-1 flex flex-wrap justify-end gap-1">
              {translations.slice(0, 6).map((translation) => (
                <span key={translation} className="rounded-full bg-surface-raised px-2 py-1 text-xs text-ink">
                  {translation}
                </span>
              ))}
            </div>
          </div>
        ) : null}
      </div>

      {mainSense?.definition ? (
        <div>
          <div className="text-[10px] uppercase tracking-wide text-muted">Definition</div>
          <p className="mt-1 text-sm text-ink">{mainSense.definition}</p>
        </div>
      ) : null}

      {examples.length ? (
        <div>
          <div className="text-[10px] uppercase tracking-wide text-muted">Example</div>
          <blockquote className="mt-1 rounded-lg border border-line bg-surface-field px-3 py-2 text-sm text-ink">
            {examples[0]}
          </blockquote>
        </div>
      ) : null}

      {(mainSense?.register || mainSense?.domain || mainSense?.frequency_band || synonyms.length || antonyms.length) ? (
        <div className="grid gap-3 sm:grid-cols-2">
          <div className="space-y-2">
            {mainSense?.register ? <p className="text-xs text-muted">Register: <span className="text-ink">{mainSense.register}</span></p> : null}
            {mainSense?.domain ? <p className="text-xs text-muted">Domain: <span className="text-ink">{mainSense.domain}</span></p> : null}
            {mainSense?.frequency_band ? <p className="text-xs text-muted">Frequency: <span className="text-ink">{mainSense.frequency_band}</span></p> : null}
          </div>
          <div className="space-y-2">
            {synonyms.length ? (
              <p className="text-xs text-muted">
                Synonyms: <span className="text-ink">{synonyms.join(', ')}</span>
              </p>
            ) : null}
            {antonyms.length ? (
              <p className="text-xs text-muted">
                Antonyms: <span className="text-ink">{antonyms.join(', ')}</span>
              </p>
            ) : null}
          </div>
        </div>
      ) : null}

      {additionalSenses.length ? (
        <div>
          <div className="text-[10px] uppercase tracking-wide text-muted">More senses</div>
          <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-muted">
            {additionalSenses.map((sense, index) => (
              <li key={sense.sense_id ?? `${entry.lemma}-sense-${index}`}>{sense.definition}</li>
            ))}
          </ul>
        </div>
      ) : null}

      {entry.etymology ? (
        <details className="rounded-lg border border-line bg-surface-field px-3 py-2">
          <summary className="cursor-pointer text-xs font-medium uppercase tracking-wide text-muted">Etymology</summary>
          <p className="mt-2 text-sm text-muted">{entry.etymology}</p>
        </details>
      ) : null}

      {showConjugation && isSpanishVerbItem(item) ? <SpanishConjugationTable item={item} /> : null}
    </article>
  );
}
