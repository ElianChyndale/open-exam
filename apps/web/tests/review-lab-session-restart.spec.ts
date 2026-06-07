import { expect, test } from '@playwright/test';
import { mkdirSync, writeFileSync } from 'fs';
import { join } from 'path';

function seedDailyReviewSnapshot(root: string) {
  const snapshotRoot = join(root, '.system', 'memory', 'review', 'daily');
  mkdirSync(snapshotRoot, { recursive: true });
  const payload = {
    review_id: 'playwright-review',
    generated_for: '2026-06-07',
    knowledge_points: [
      {
        knowledge_id: 'pw-kp-1',
        subject: 'Corporate Issuers',
        heading: 'Capital Structure',
        trigger: 'Recall the trade-off theory intuition.',
        decision: 'Tax shields are balanced against expected distress costs.',
        priority: 90,
        reason: 'Due today',
        state: 'Learning',
        source_refs: ['playwright/corporate-issuers'],
      },
    ],
    mistake_cards: [],
  };
  const text = JSON.stringify(payload, null, 2);
  writeFileSync(join(snapshotRoot, 'playwright-review.json'), text, 'utf-8');
  writeFileSync(join(snapshotRoot, 'latest.json'), text, 'utf-8');
}

test.beforeEach(async ({}, testInfo) => {
  const root = String(testInfo.config.metadata.openexamDataRoot);
  seedDailyReviewSnapshot(root);
});

test('start new session leaves completion state and returns to active review', async ({ page }) => {
  const created = await page.request.post('/api/review-lab/sessions', {
    data: {
      review_id: 'playwright-review',
      energy_level: 2,
      focus_topic: 'Corporate Issuers',
      max_units: 1,
    },
  });
  expect(created.ok()).toBeTruthy();
  const sessionId = (await created.json()).session_id as string;

  await page.goto(`/review/lab?session=${sessionId}`);

  const revealButton = page.getByRole('button', { name: /Reveal (Answer|Formula)/i });

  await expect(page.getByRole('heading', { name: 'Review Lab' })).toBeVisible();
  await expect(revealButton).toBeVisible();

  await revealButton.click();
  await page.getByRole('button', { name: /3\s*Recalled/i }).click();

  await expect(page.getByRole('heading', { name: 'All done!' })).toBeVisible();
  await page.getByRole('button', { name: 'Start New Session' }).click();

  await expect(page.getByRole('heading', { name: 'All done!' })).toBeHidden();
  await expect(page.getByRole('button', { name: /Reveal (Answer|Formula)/i })).toBeVisible();
  await expect(page).toHaveURL(/\/review\/lab\?session=/);
});
