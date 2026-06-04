import type { DictionaryResult } from '@/lib/api';

export type DictionaryInflectionValue = string | Record<string, unknown>;

export interface DictionarySenseLike {
  sense_id?: string;
  definition?: string;
  examples?: string[];
  synonyms?: string[];
  antonyms?: string[];
  register?: string;
  domain?: string;
  cefr_level?: string;
  frequency_band?: string;
  translations?: Array<{
    target_lemma?: string;
    target_language?: string;
    sense_qualifier?: string;
    confidence?: number;
    verified?: boolean;
  }>;
}

export interface DictionaryEntryLike {
  entry_id?: string;
  lemma?: string;
  pos?: string;
  language?: string;
  source_id?: string;
  etymology?: string;
  pronunciation?: string;
  audio_ref?: string;
  inflections?: DictionaryInflectionValue[];
  gender?: string;
  gender_invariable?: boolean;
  senses?: DictionarySenseLike[];
}

type ConjugationTense = 'present' | 'preterite' | 'imperfect' | 'future' | 'conditional';
type PronounKey = 'yo' | 'tú' | 'él/ella' | 'nosotros' | 'vosotros' | 'ellos/ellas';
type ConjugationForms = Record<PronounKey, string>;

const PRONOUNS: PronounKey[] = ['yo', 'tú', 'él/ella', 'nosotros', 'vosotros', 'ellos/ellas'];
const TENSES: ConjugationTense[] = ['present', 'preterite', 'imperfect', 'future', 'conditional'];

const TENSE_LABELS: Record<ConjugationTense, string> = {
  present: 'Present',
  preterite: 'Preterite',
  imperfect: 'Imperfect',
  future: 'Future',
  conditional: 'Conditional',
};

const AR_ENDINGS: Record<ConjugationTense, ConjugationForms> = {
  present: { yo: 'o', tú: 'as', 'él/ella': 'a', nosotros: 'amos', vosotros: 'áis', 'ellos/ellas': 'an' },
  preterite: { yo: 'é', tú: 'aste', 'él/ella': 'ó', nosotros: 'amos', vosotros: 'asteis', 'ellos/ellas': 'aron' },
  imperfect: { yo: 'aba', tú: 'abas', 'él/ella': 'aba', nosotros: 'ábamos', vosotros: 'abais', 'ellos/ellas': 'aban' },
  future: { yo: 'aré', tú: 'arás', 'él/ella': 'ará', nosotros: 'aremos', vosotros: 'aréis', 'ellos/ellas': 'arán' },
  conditional: { yo: 'aría', tú: 'arías', 'él/ella': 'aría', nosotros: 'aríamos', vosotros: 'aríais', 'ellos/ellas': 'arían' },
};

const ER_ENDINGS: Record<ConjugationTense, ConjugationForms> = {
  present: { yo: 'o', tú: 'es', 'él/ella': 'e', nosotros: 'emos', vosotros: 'éis', 'ellos/ellas': 'en' },
  preterite: { yo: 'í', tú: 'iste', 'él/ella': 'ió', nosotros: 'imos', vosotros: 'isteis', 'ellos/ellas': 'ieron' },
  imperfect: { yo: 'ía', tú: 'ías', 'él/ella': 'ía', nosotros: 'íamos', vosotros: 'íais', 'ellos/ellas': 'ían' },
  future: { yo: 'eré', tú: 'erás', 'él/ella': 'erá', nosotros: 'eremos', vosotros: 'eréis', 'ellos/ellas': 'erán' },
  conditional: { yo: 'ería', tú: 'erías', 'él/ella': 'ería', nosotros: 'eríamos', vosotros: 'eríais', 'ellos/ellas': 'erían' },
};

const IR_ENDINGS: Record<ConjugationTense, ConjugationForms> = {
  present: { yo: 'o', tú: 'es', 'él/ella': 'e', nosotros: 'imos', vosotros: 'ís', 'ellos/ellas': 'en' },
  preterite: { yo: 'í', tú: 'iste', 'él/ella': 'ió', nosotros: 'imos', vosotros: 'isteis', 'ellos/ellas': 'ieron' },
  imperfect: { yo: 'ía', tú: 'ías', 'él/ella': 'ía', nosotros: 'íamos', vosotros: 'íais', 'ellos/ellas': 'ían' },
  future: { yo: 'iré', tú: 'irás', 'él/ella': 'irá', nosotros: 'iremos', vosotros: 'iréis', 'ellos/ellas': 'irán' },
  conditional: { yo: 'iría', tú: 'irías', 'él/ella': 'iría', nosotros: 'iríamos', vosotros: 'iríais', 'ellos/ellas': 'irían' },
};

const STEM_CHANGES: Record<string, [string, string]> = {
  pensar: ['e', 'ie'],
  querer: ['e', 'ie'],
  entender: ['e', 'ie'],
  perder: ['e', 'ie'],
  cerrar: ['e', 'ie'],
  empezar: ['e', 'ie'],
  nevar: ['e', 'ie'],
  sentar: ['e', 'ie'],
  poder: ['o', 'ue'],
  dormir: ['o', 'ue'],
  volver: ['o', 'ue'],
  encontrar: ['o', 'ue'],
  morir: ['o', 'ue'],
  mover: ['o', 'ue'],
  recordar: ['o', 'ue'],
  resolver: ['o', 'ue'],
  sonar: ['o', 'ue'],
  contar: ['o', 'ue'],
  pedir: ['e', 'i'],
  servir: ['e', 'i'],
  repetir: ['e', 'i'],
  seguir: ['e', 'i'],
  vestir: ['e', 'i'],
};

const IRREGULAR_YO: Record<string, string> = {
  ser: 'soy',
  estar: 'estoy',
  ir: 'voy',
  tener: 'tengo',
  venir: 'vengo',
  hacer: 'hago',
  decir: 'digo',
  traer: 'traigo',
  caer: 'caigo',
  poner: 'pongo',
  salir: 'salgo',
  valer: 'valgo',
  saber: 'sé',
  ver: 'veo',
  dar: 'doy',
  conocer: 'conozco',
  conducir: 'conduzco',
  producir: 'produzco',
  traducir: 'traduzco',
  caber: 'quepo',
  haber: 'he',
};

const IRREGULAR_PRESENT: Record<string, ConjugationForms> = {
  ser: { yo: 'soy', tú: 'eres', 'él/ella': 'es', nosotros: 'somos', vosotros: 'sois', 'ellos/ellas': 'son' },
  estar: { yo: 'estoy', tú: 'estás', 'él/ella': 'está', nosotros: 'estamos', vosotros: 'estáis', 'ellos/ellas': 'están' },
  ir: { yo: 'voy', tú: 'vas', 'él/ella': 'va', nosotros: 'vamos', vosotros: 'vais', 'ellos/ellas': 'van' },
  tener: { yo: 'tengo', tú: 'tienes', 'él/ella': 'tiene', nosotros: 'tenemos', vosotros: 'tenéis', 'ellos/ellas': 'tienen' },
  venir: { yo: 'vengo', tú: 'vienes', 'él/ella': 'viene', nosotros: 'venimos', vosotros: 'venís', 'ellos/ellas': 'vienen' },
  decir: { yo: 'digo', tú: 'dices', 'él/ella': 'dice', nosotros: 'decimos', vosotros: 'decís', 'ellos/ellas': 'dicen' },
  hacer: { yo: 'hago', tú: 'haces', 'él/ella': 'hace', nosotros: 'hacemos', vosotros: 'hacéis', 'ellos/ellas': 'hacen' },
  haber: { yo: 'he', tú: 'has', 'él/ella': 'ha', nosotros: 'hemos', vosotros: 'habéis', 'ellos/ellas': 'han' },
};

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

function resolveEntry(item: DictionaryResult | DictionaryEntryLike): DictionaryEntryLike {
  if (!isDictionaryResult(item)) {
    return item;
  }
  return (
    safeParseEntryJson(item.entry_json) ?? {
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
    }
  );
}

function classifyVerb(infinitive: string): 'ar' | 'er' | 'ir' | 'irregular' {
  if (IRREGULAR_PRESENT[infinitive]) return 'irregular';
  if (infinitive.endsWith('ar')) return 'ar';
  if (infinitive.endsWith('er')) return 'er';
  if (infinitive.endsWith('ir')) return 'ir';
  return 'irregular';
}

function replaceLast(source: string, searchValue: string, replaceValue: string): string {
  const index = source.lastIndexOf(searchValue);
  if (index < 0) return source;
  return `${source.slice(0, index)}${replaceValue}${source.slice(index + searchValue.length)}`;
}

function buildGeneratedForms(lemma: string, tense: ConjugationTense): ConjugationForms | null {
  const infinitive = lemma.toLowerCase().trim();
  if (!infinitive) return null;

  if (tense === 'present' && IRREGULAR_PRESENT[infinitive]) {
    return IRREGULAR_PRESENT[infinitive];
  }

  const verbClass = classifyVerb(infinitive);
  const endings =
    verbClass === 'ar' ? AR_ENDINGS[tense] :
    verbClass === 'er' ? ER_ENDINGS[tense] :
    verbClass === 'ir' ? IR_ENDINGS[tense] :
    AR_ENDINGS.present;

  let stem = verbClass === 'irregular' ? infinitive : infinitive.slice(0, -2);
  if (tense === 'present' && STEM_CHANGES[infinitive]) {
    const [from, to] = STEM_CHANGES[infinitive];
    stem = replaceLast(stem, from, to);
  }

  const forms = PRONOUNS.reduce((acc, pronoun) => {
    acc[pronoun] = `${stem}${endings[pronoun]}`;
    return acc;
  }, {} as ConjugationForms);

  if (tense === 'present' && IRREGULAR_YO[infinitive]) {
    forms.yo = IRREGULAR_YO[infinitive];
  }
  return forms;
}

function emptyForms(): ConjugationForms {
  return {
    yo: '',
    tú: '',
    'él/ella': '',
    nosotros: '',
    vosotros: '',
    'ellos/ellas': '',
  };
}

function toPronounValue(value: unknown): Partial<ConjugationForms> {
  if (!value || typeof value !== 'object') return {};
  const record = value as Record<string, unknown>;
  const normalized: Partial<ConjugationForms> = {};
  for (const pronoun of PRONOUNS) {
    const direct = record[pronoun];
    if (typeof direct === 'string' && direct.trim()) {
      normalized[pronoun] = direct.trim();
    }
  }
  return normalized;
}

function formsFromInflections(
  inflections: DictionaryInflectionValue[] | undefined,
  tense: ConjugationTense,
): ConjugationForms | null {
  if (!inflections?.length) return null;

  for (const value of inflections) {
    if (typeof value === 'string') {
      if (tense !== 'present') continue;
      const [label, form] = value.split(':', 2);
      if (!label || !form) continue;
      const pronoun = label.trim() as PronounKey;
      if (!PRONOUNS.includes(pronoun)) continue;
      const generated = emptyForms();
      generated[pronoun] = form.trim();
      return generated;
    }

    const record = value as Record<string, unknown>;
    const candidateTense = typeof record.tense === 'string' ? record.tense.toLowerCase() : '';
    const candidateMood = typeof record.mood === 'string' ? record.mood.toLowerCase() : '';
    const nested = record.verb_forms;

    if (candidateTense && candidateTense !== tense) continue;
    if (candidateMood && candidateMood !== 'indicative') continue;

    const explicit = {
      ...toPronounValue(record),
      ...toPronounValue(nested),
    };
    if (Object.keys(explicit).length) {
      const base = emptyForms();
      return { ...base, ...explicit };
    }
  }

  return null;
}

export function isSpanishVerbItem(item: DictionaryResult | DictionaryEntryLike): boolean {
  const entry = resolveEntry(item);
  return entry.language === 'es' && entry.pos === 'verb' && Boolean(entry.lemma);
}

export function getSpanishConjugations(
  item: DictionaryResult | DictionaryEntryLike,
): Array<{ tense: ConjugationTense; forms: ConjugationForms; source: 'entry' | 'generated' }> {
  const entry = resolveEntry(item);
  const lemma = entry.lemma?.trim();
  if (!lemma || entry.language !== 'es' || entry.pos !== 'verb') {
    return [];
  }

  return TENSES.map((tense) => {
    const explicit = formsFromInflections(entry.inflections, tense);
    if (explicit) {
      return { tense, forms: explicit, source: 'entry' as const };
    }
    const generated = buildGeneratedForms(lemma, tense);
    return generated ? { tense, forms: generated, source: 'generated' as const } : null;
  }).filter((value): value is { tense: ConjugationTense; forms: ConjugationForms; source: 'entry' | 'generated' } => Boolean(value));
}

export function SpanishConjugationTable({
  item,
}: {
  item: DictionaryResult | DictionaryEntryLike;
}) {
  const entry = resolveEntry(item);
  const sections = getSpanishConjugations(item);

  if (!sections.length || !entry.lemma) {
    return null;
  }

  return (
    <div className="rounded-xl border border-line bg-surface-raised/40 p-4">
      <div className="mb-3 flex items-center justify-between gap-2">
        <div>
          <h4 className="text-sm font-semibold text-ink">Spanish conjugation</h4>
          <p className="text-xs text-muted">
            Indicative forms for <span className="font-medium text-ink">{entry.lemma}</span>
          </p>
        </div>
        <span className="rounded-full border border-line px-2 py-1 text-[10px] uppercase tracking-wide text-muted">
          {sections.some((section) => section.source === 'entry') ? 'entry-backed' : 'rule-generated'}
        </span>
      </div>

      <div className="space-y-4">
        {sections.map((section) => (
          <div key={section.tense} className="overflow-hidden rounded-lg border border-line">
            <div className="flex items-center justify-between bg-surface px-3 py-2">
              <span className="text-xs font-medium uppercase tracking-wide text-muted">
                {TENSE_LABELS[section.tense]}
              </span>
              <span className="text-[10px] text-muted">
                {section.source === 'entry' ? 'from entry data' : 'from local morphology rules'}
              </span>
            </div>
            <div className="grid grid-cols-2 gap-px bg-line sm:grid-cols-3">
              {PRONOUNS.map((pronoun) => (
                <div key={`${section.tense}-${pronoun}`} className="bg-surface-field px-3 py-2">
                  <div className="text-[10px] uppercase tracking-wide text-muted">{pronoun}</div>
                  <div className="mt-1 text-sm text-ink">{section.forms[pronoun] || '—'}</div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
