'use client';

import { useState } from 'react';

const STEPS = [
  { step: 1, title: 'Import your first article', description: 'Add a text, URL, or paste content to start building your vocabulary.', action: 'Import content', href: '/language/import' },
  { step: 2, title: 'Review extracted terms', description: 'See which words and phrases were automatically extracted from your content.', action: 'Open corpus', href: '/language/corpus' },
  { step: 3, title: 'Start your first review', description: 'Practice with spaced repetition cards. Just 5 minutes a day builds lasting memory.', action: 'Start review', href: '/language/review' },
];

export function GuidedOnboarding({ onDismiss }: { onDismiss?: () => void }) {
  const [currentStep, setCurrentStep] = useState(0);

  if (currentStep >= STEPS.length) return null;

  const step = STEPS[currentStep];
  return (
    <div className="rounded-2xl border border-accent/30 bg-accent-soft/10 p-6">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wider text-accent">Welcome to LanguageOS</p>
          <h3 className="mt-2 text-lg font-bold">Step {step.step} of {STEPS.length}</h3>
          <h4 className="mt-1 text-xl font-semibold">{step.title}</h4>
          <p className="mt-2 text-sm text-muted max-w-md">{step.description}</p>
        </div>
        <div className="flex items-center gap-1">
          {STEPS.map((_, i) => (
            <div key={i} className={`h-2 w-2 rounded-full ${i === currentStep ? 'bg-accent' : 'bg-line'}`} />
          ))}
        </div>
      </div>
      <div className="mt-4 flex gap-3">
        <a href={step.href} className="btn-primary text-sm">{step.action}</a>
        <button
          type="button"
          onClick={() => {
            if (currentStep < STEPS.length - 1) setCurrentStep(currentStep + 1);
            else onDismiss?.();
          }}
          className="btn-secondary text-sm"
        >
          {currentStep < STEPS.length - 1 ? 'Skip' : 'Got it'}
        </button>
      </div>
    </div>
  );
}
