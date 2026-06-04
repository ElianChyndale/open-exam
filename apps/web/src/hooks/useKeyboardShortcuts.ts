'use client';

import { useEffect, useCallback } from 'react';

export type ShortcutAction =
  | 'reveal'
  | 'submit'
  | 'rate-forgot'
  | 'rate-partial'
  | 'rate-recalled'
  | 'rate-skipped'
  | 'hint'
  | 'help'
  | 'pause'
  | 'resume'
  | 'next'
  | 'prev';

interface UseKeyboardShortcutsOptions {
  enabled?: boolean;
  onAction: (action: ShortcutAction) => void;
  revealed?: boolean;
  paused?: boolean;
}

/**
 * Keyboard shortcuts for the Review Lab.
 *
 * R / Space  = reveal answer (only when not revealed)
 * Ctrl+Enter = reveal/submit primary action
 * 1          = forgot
 * 2          = partial
 * 3          = recalled
 * S / 4      = skip
 * N          = next
 * ?          = shortcut help
 * H          = hint
 * P          = pause / resume
 */
export function useKeyboardShortcuts({
  enabled = true,
  onAction,
  revealed = false,
  paused = false,
}: UseKeyboardShortcutsOptions) {
  const handleKeyDown = useCallback(
    (e: KeyboardEvent) => {
      if (!enabled) return;

      const target = e.target as HTMLElement;
      const primarySubmit = e.key === 'Enter' && (e.ctrlKey || e.metaKey);
      const key = e.key.toLowerCase();
      const isTextEntry =
        target.tagName === 'INPUT' ||
        target.tagName === 'TEXTAREA' ||
        target.tagName === 'SELECT' ||
        target.isContentEditable;
      const isClickable =
        target.tagName === 'BUTTON' ||
        target.tagName === 'A';
      if (isTextEntry && !primarySubmit) {
        return;
      }
      if (isClickable && (key === ' ' || key === 'enter') && !primarySubmit) {
        return;
      }

      if (primarySubmit) {
        e.preventDefault();
        if (!paused) onAction(revealed ? 'submit' : 'reveal');
        return;
      }

      switch (key) {
        case '?':
          e.preventDefault();
          onAction('help');
          break;
        case ' ':
        case 'r':
          e.preventDefault();
          if (!revealed && !paused) {
            onAction('reveal');
          }
          break;
        case '1':
          if (revealed && !paused) onAction('rate-forgot');
          break;
        case '2':
          if (revealed && !paused) onAction('rate-partial');
          break;
        case '3':
          if (revealed && !paused) onAction('rate-recalled');
          break;
        case '4':
        case 's':
          if (revealed && !paused) onAction('rate-skipped');
          break;
        case 'n':
          if (!paused) onAction('next');
          break;
        case 'h':
          if (!paused) onAction('hint');
          break;
        case 'p':
          onAction(paused ? 'resume' : 'pause');
          break;
        default:
          break;
      }
    },
    [enabled, onAction, revealed, paused]
  );

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [handleKeyDown]);
}
