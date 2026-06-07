import { expect, test } from '@playwright/test';

test('global assistant launcher opens on every page and stays open across navigation', async ({ page }) => {
  await page.goto('/today');
  await page.getByRole('button', { name: /Open AI assistant/i }).click();
  await expect(page.getByRole('complementary', { name: /AI Assistant/i })).toBeVisible();

  await page.getByRole('link', { name: /Daily Review/i }).click();
  await expect(page).toHaveURL(/\/review$/);
  await expect(page.getByRole('complementary', { name: /AI Assistant/i })).toBeVisible();
});
