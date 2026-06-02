import { expect, test } from '@playwright/test';

test('Resource Center exposes local provider health and explicit scheduler status', async ({ page }) => {
  await page.goto('/resources');

  await expect(page.getByRole('heading', { name: '资源中心' })).toBeVisible();
  await expect(page.getByText('Generic Web')).toBeVisible();
  await expect(page.getByText('未安装，需要显式安装')).toBeVisible();
  await expect(page.getByText('.\\scripts\\install-resource-scheduler.ps1')).toBeVisible();
  await expect(page.getByText('OpenAI Web Search consent：未授权')).toBeVisible();
  await expect(page.getByRole('heading', { name: '任务队列' })).toBeVisible();
  await expect(page.getByRole('heading', { name: '来源目录' })).toBeVisible();
  await expect(page.getByRole('heading', { name: '审计中心' })).toBeVisible();
});
