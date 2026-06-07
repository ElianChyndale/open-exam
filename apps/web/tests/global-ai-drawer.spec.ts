import { expect, test } from '@playwright/test';

test('global assistant launcher opens on every page and stays open across navigation', async ({ page }) => {
  await page.goto('/today');
  await page.getByRole('button', { name: /Open AI assistant/i }).click();
  await expect(page.getByRole('complementary', { name: /AI Assistant/i })).toBeVisible();

  await page.getByRole('link', { name: /Daily Review/i }).click();
  await expect(page).toHaveURL(/\/review$/);
  await expect(page.getByRole('complementary', { name: /AI Assistant/i })).toBeVisible();
});

test('assistant conversation persists across page navigation', async ({ page }) => {
  await page.goto('/today');
  await page.getByRole('button', { name: /Open AI assistant/i }).click();
  await page.getByLabel('Assistant message').fill('Open Review Lab');
  await page.getByRole('button', { name: /Send/i }).click();
  await expect(page.getByText('Open Review Lab')).toBeVisible();

  await page.getByRole('link', { name: /Daily Review/i }).click();
  await expect(page.getByText('Open Review Lab')).toBeVisible();
});

test('assistant drawer shows action result cards for capture and commands', async ({ page }) => {
  await page.goto('/review');
  await page.getByRole('button', { name: /Open AI assistant/i }).click();

  await page.getByLabel('Assistant message').fill('Open Review Lab');
  await page.getByRole('button', { name: /Send/i }).click();
  await expect(page.getByText('Opened Review Lab.')).toBeVisible();

  await page.getByLabel('Assistant message').fill('I got this wrong. Topic: Financial Statement Analysis. LOS: FSA.2.2. Question: common-size balance sheet cash. Wrong answer: 20%. Correct answer: 25%.');
  await page.getByRole('button', { name: /Send/i }).click();
  await expect(page.getByText(/Recorded this as question evidence/i)).toBeVisible();
});
