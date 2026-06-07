import { mkdirSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { spawnSync } from 'node:child_process';

const result = spawnSync('npx', ['next', 'typegen'], {
  stdio: 'inherit',
  shell: true,
});

if (result.status !== 0) {
  process.exit(result.status ?? 1);
}

const shimPath = resolve('.next/types/routes.js');
mkdirSync(dirname(shimPath), { recursive: true });
writeFileSync(shimPath, 'export {};\n', 'utf8');
