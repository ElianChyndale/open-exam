'use client';

import { type FormEvent, useState } from 'react';

export function TypingInput({
  prompt,
  expected,
  onSubmit,
}: {
  prompt: string;
  expected: string;
  onSubmit: (input: string, score: number) => void;
}) {
  const [value, setValue] = useState('');
  const [revealed, setRevealed] = useState(false);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (!value.trim()) return;
    const score = fuzzyMatch(value, expected);
    setRevealed(true);
    onSubmit(value, score);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <p className="text-sm font-medium">{prompt}</p>
      {!revealed ? (
        <div className="flex gap-2">
          <input
            value={value}
            onChange={(e) => setValue(e.target.value)}
            className="input flex-1"
            placeholder="Type your answer..."
            autoFocus
          />
          <button type="submit" className="btn-primary text-sm">Check</button>
        </div>
      ) : (
        <div className="space-y-2">
          <p className="text-sm">Your answer: <span className={fuzzyMatch(value, expected) >= 0.8 ? 'text-green-600' : 'text-red-600'}>{value}</span></p>
          <p className="text-sm text-muted">Expected: {expected}</p>
        </div>
      )}
    </form>
  );
}

function fuzzyMatch(actual: string, expected: string): number {
  const a = actual.toLowerCase().trim();
  const b = expected.toLowerCase().trim();
  if (a === b) return 1.0;
  let matches = 0;
  for (let i = 0; i < Math.min(a.length, b.length); i++) {
    if (a[i] === b[i]) matches++;
  }
  return Math.min(1.0, matches / Math.max(a.length, b.length));
}
