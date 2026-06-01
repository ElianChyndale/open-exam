import { expect, test } from '@playwright/test';

test('LanguageOS capture, collect, review, grammar, and graph flow', async ({ page }) => {
  await page.goto('/language/import');
  await page.getByPlaceholder('Source title').fill('Playwright finance context');
  await page.getByPlaceholder('Paste text, subtitle content, extracted document text, or local audio placeholder.').fill(
    'The issuance of new shares may have a dilutive effect on EPS.',
  );
  await page.getByRole('button', { name: 'Capture source' }).click();
  await expect(page.getByRole('status')).toContainText(/Captured|Already captured/);

  await page.goto('/language/corpus');
  await page.getByPlaceholder('Expression to collect').fill('dilutive effect');
  await page.locator('select[required]').selectOption({ index: 1 });
  await page.getByRole('button', { name: 'Collect' }).click();
  await expect(page.getByRole('status')).toContainText(/Collected|Merged/);
  await expect(page.getByText('dilutive effect', { exact: true })).toBeVisible();

  await page.goto('/language/review');
  await page.getByRole('button', { name: 'Generate cards from first corpus item' }).click();
  await expect(page.locator('.language-review-card')).toBeVisible();
  await page.locator('.language-review-card').click();
  await page.getByRole('button', { name: 'good' }).click();
  await expect(page.getByRole('status')).toContainText('Next review');

  await page.goto('/language/grammar');
  await page.getByRole('button', { name: 'Analyze sentence' }).click();
  await expect(page.getByRole('status')).toContainText(/Created|Loaded/);
  await expect(page.locator('.grammar-node').first()).toBeVisible();

  await page.goto('/language/intuition');
  await page.getByRole('button', { name: 'Rebuild deterministic graph' }).click();
  await page.getByPlaceholder('Search meaning or expression').fill('dilutive');
  await page.getByRole('button', { name: 'Search' }).click();
  await expect(page.getByText('dilutive effect', { exact: true })).toBeVisible();
});

test('reduced motion disables optional GSAP page movement', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/language');
  await expect(page.locator('[data-motion-enabled]')).toHaveAttribute('data-motion-enabled', 'false');
  await expect(page.locator('.language-hero')).toBeVisible();
});
