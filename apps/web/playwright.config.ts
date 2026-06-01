import { defineConfig } from '@playwright/test';
import { resolve } from 'path';

const dataRoot = resolve(__dirname, '../../.playwright-data');

export default defineConfig({
  testDir: './tests',
  timeout: 30_000,
  use: {
    baseURL: 'http://127.0.0.1:3010',
    trace: 'retain-on-failure',
  },
  webServer: [
    {
      command: 'python -m uvicorn main:app --host 127.0.0.1 --port 8000',
      cwd: resolve(__dirname, '../api'),
      env: { OPENEXAM_REPO_ROOT: dataRoot },
      url: 'http://127.0.0.1:8000/api/health',
      reuseExistingServer: true,
      timeout: 120_000,
    },
    {
      command: 'npm run dev -- --hostname 127.0.0.1 --port 3010',
      cwd: __dirname,
      url: 'http://127.0.0.1:3010/language',
      reuseExistingServer: true,
      timeout: 120_000,
    },
  ],
});
