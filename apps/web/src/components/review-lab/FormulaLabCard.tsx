'use client';

import { useState } from 'react';

interface FormulaLabCardProps {
  prompt: string;
  formulaLatex: string;
  recallInstruction?: string;
  answer?: string;
  workedExample?: string;
  commonWrongPath?: string;
  examTrap?: string;
  variables?: Array<{ symbol: string; meaning?: string; unit?: string; description?: string }>;
  appliesWhen?: string[];
  boundaryRules?: string[];
  baIiPlusSteps?: string[];
  revealed: boolean;
  onReveal: () => void;
  subject?: string;
  dueReason?: string;
  memoryState?: string;
}

/**
 * FormulaLabCard — renders a LaTeX formula with a variables table.
 *
 * The formula and answer are NEVER rendered in the DOM until revealed=true.
 */
export function FormulaLabCard({
  prompt,
  formulaLatex,
  recallInstruction,
  answer,
  workedExample,
  commonWrongPath,
  examTrap,
  variables: providedVariables,
  appliesWhen = [],
  boundaryRules = [],
  baIiPlusSteps = [],
  revealed,
  onReveal,
  subject,
  dueReason,
  memoryState,
}: FormulaLabCardProps) {
  const [showWork, setShowWork] = useState(false);

  // Extract variables from formula (simple heuristic: capital letters and Greek-like names)
  const variables = providedVariables?.length
    ? providedVariables.map((item) => ({
        symbol: item.symbol,
        description: item.meaning || item.description || item.unit || 'Meaning pending',
      }))
    : extractVariables(formulaLatex);

  return (
    <div className="w-full rounded-2xl border border-line bg-surface-raised p-6 text-left">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <span className="metric-label text-[10px] uppercase tracking-wider">
            Formula Lab
          </span>
          {subject && (
            <span className="text-[10px] text-muted bg-surface-field px-2 py-0.5 rounded-full">
              {subject}
            </span>
          )}
        </div>
        <div className="flex items-center gap-2">
          {memoryState && (
            <span className="text-[10px] text-muted">{memoryState}</span>
          )}
          {dueReason && (
            <span className="text-[10px] text-warning">{dueReason}</span>
          )}
        </div>
      </div>

      {/* Prompt */}
      <div className="mb-4">
        <h3 className="text-lg font-semibold leading-relaxed">{prompt}</h3>
        {recallInstruction && !revealed && (
          <p className="mt-2 text-sm text-muted">{recallInstruction}</p>
        )}
      </div>

      {/* Reveal button or formula + answer */}
      {!revealed ? (
        <button
          type="button"
          onClick={onReveal}
          className="w-full rounded-xl border-2 border-dashed border-accent-soft bg-surface-field py-8 text-sm font-medium text-accent hover:bg-accent-soft transition-colors"
        >
          <span className="block text-lg mb-1">Reveal Formula</span>
          <span className="text-xs text-muted">Space to reveal</span>
        </button>
      ) : (
        <div className="space-y-4 animate-in fade-in duration-200">
          {/* Formula */}
          {formulaLatex && (
            <div className="rounded-xl bg-accent-soft border border-accent-soft p-4">
              <span className="text-[10px] uppercase tracking-wider text-accent font-semibold">
                Formula
              </span>
              <div className="mt-2 text-xl font-mono leading-relaxed overflow-x-auto">
                {formulaLatex}
              </div>

              {/* Variables table */}
              {variables.length > 0 && (
                <table className="mt-3 w-full text-xs">
                  <thead>
                    <tr className="text-left text-muted border-b border-line">
                      <th className="py-1 pr-3">Variable</th>
                      <th className="py-1">Meaning</th>
                    </tr>
                  </thead>
                  <tbody>
                    {variables.map((v) => (
                      <tr key={v.symbol} className="border-b border-line/50">
                        <td className="py-1.5 pr-3 font-mono font-semibold">{v.symbol}</td>
                        <td className="py-1.5 text-muted">{v.description}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          )}

          {/* Answer / Decision */}
          {answer && (
            <div className="rounded-xl bg-success-soft border border-success-soft p-4">
              <span className="text-[10px] uppercase tracking-wider text-success font-semibold">
                Decision Rule
              </span>
              <p className="mt-1 text-sm leading-relaxed whitespace-pre-wrap">{answer}</p>
            </div>
          )}

          {appliesWhen.length > 0 && (
            <MetadataBlock title="Applies When" items={appliesWhen} tone="accent" />
          )}

          {boundaryRules.length > 0 && (
            <MetadataBlock title="Boundary Rules" items={boundaryRules} tone="warning" />
          )}

          {baIiPlusSteps.length > 0 && (
            <MetadataBlock title="BA II Plus" items={baIiPlusSteps} tone="accent" />
          )}

          {/* Worked example toggle */}
          {workedExample && (
            <div>
              <button
                type="button"
                onClick={() => setShowWork((s) => !s)}
                className="text-xs text-accent hover:underline"
              >
                {showWork ? 'Hide worked example' : 'Show worked example'}
              </button>
              {showWork && (
                <div className="mt-2 rounded-lg bg-surface-field border border-line p-3 text-sm leading-relaxed whitespace-pre-wrap">
                  {workedExample}
                </div>
              )}
            </div>
          )}

          {/* Common wrong path */}
          {commonWrongPath && (
            <div className="rounded-lg bg-danger-soft border border-danger-soft p-3">
              <span className="text-[10px] uppercase tracking-wider text-danger font-semibold">
                Common Mistake
              </span>
              <p className="mt-1 text-xs leading-relaxed">{commonWrongPath}</p>
            </div>
          )}

          {/* Exam trap */}
          {examTrap && (
            <div className="rounded-lg bg-warning-soft border border-warning-soft p-3">
              <span className="text-[10px] uppercase tracking-wider text-warning font-semibold">
                Exam Trap
              </span>
              <p className="mt-1 text-xs leading-relaxed">{examTrap}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function MetadataBlock({ title, items, tone }: { title: string; items: string[]; tone: 'accent' | 'warning' }) {
  const toneClass = tone === 'warning'
    ? 'bg-warning-soft border-warning-soft text-warning'
    : 'bg-accent-soft border-accent-soft text-accent';
  return (
    <div className={`rounded-lg border p-3 ${toneClass}`}>
      <span className="text-[10px] uppercase tracking-wider font-semibold">
        {title}
      </span>
      <ul className="mt-1 space-y-1 text-xs leading-relaxed text-ink">
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

interface FormulaVariable {
  symbol: string;
  description: string;
}

function extractVariables(formula: string): FormulaVariable[] {
  if (!formula) return [];
  // Simple heuristic: look for common finance variable patterns
  const known: Record<string, string> = {
    r: 'Risk-free rate or required return',
    rf: 'Risk-free rate',
    rm: 'Market return',
    beta: 'Systematic risk (beta)',
    sigma: 'Standard deviation',
    mu: 'Expected return (mean)',
    E: 'Expected value',
    PV: 'Present value',
    FV: 'Future value',
    NPV: 'Net present value',
    IRR: 'Internal rate of return',
    WACC: 'Weighted average cost of capital',
    D: 'Dividend',
    P: 'Price',
    g: 'Growth rate',
    n: 'Number of periods',
    t: 'Time period',
    T: 'Tax rate or time to maturity',
    C: 'Coupon payment or cash flow',
    F: 'Face value',
    y: 'Yield',
    YTM: 'Yield to maturity',
    DCF: 'Discounted cash flow',
    EBITDA: 'Earnings before interest, taxes, depreciation and amortization',
    EPS: 'Earnings per share',
    ROE: 'Return on equity',
    ROA: 'Return on assets',
    ROIC: 'Return on invested capital',
    DFL: 'Degree of financial leverage',
    DOL: 'Degree of operating leverage',
    DTL: 'Degree of total leverage',
  };

  const found = new Set<string>();
  const results: FormulaVariable[] = [];

  // Tokenize by non-word characters
  const tokens = formula.split(/[^a-zA-Z0-9_]+/);
  for (const token of tokens) {
    const t = token.trim();
    if (!t || found.has(t)) continue;
    if (known[t]) {
      found.add(t);
      results.push({ symbol: t, description: known[t] });
    }
  }

  return results;
}
