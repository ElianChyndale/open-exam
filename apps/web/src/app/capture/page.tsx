'use client';

import QuestionBankImportConsole from '@/components/capture/QuestionBankImportConsole';

export default function QuestionCapture() {
  return (
    <div className="mx-auto max-w-4xl space-y-6">
      <div>
        <h2 className="text-2xl font-bold">Capture Tools</h2>
        <p className="mt-1 text-sm text-muted">
          Normal capture now happens through the global AI assistant. This page is only for imports, fallback structured entry, and admin tools.
        </p>
      </div>
      <QuestionBankImportConsole />
    </div>
  );
}
