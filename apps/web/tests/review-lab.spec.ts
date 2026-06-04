import { expect, test } from '@playwright/test';
import { mkdirSync, writeFileSync } from 'fs';
import { join } from 'path';

const API_BASE = `http://127.0.0.1:${process.env.OPENEXAM_API_PORT || '8000'}`;

test('Review Lab is recall-first and hides prior wrong answers', async ({ page }) => {
  const wrongAnswer = 'Macaulay duration';
  const correctRule = 'Use effective duration when cash flows can change.';

  const attempt = await page.request.post(`${API_BASE}/api/attempts`, {
    data: {
      topic: 'Fixed Income',
      los: 'FI.Duration',
      prompt_or_question: 'Which duration measure fits callable bonds?',
      wrong_choice_or_output: wrongAnswer,
      correct_resolution: correctRule,
      error_type: 'concept_confusion',
      confidence: 1,
      time_spent: 60,
      evidence_refs: ['review-lab-e2e'],
      is_correct: false,
    },
  });
  expect(attempt.ok()).toBeTruthy();

  const dailyReview = await page.request.get(`${API_BASE}/api/daily-review/today`);
  expect(dailyReview.ok()).toBeTruthy();
  const reviewPayload = await dailyReview.json();

  const session = await page.request.post(`${API_BASE}/api/review-lab/generate`, {
    data: {
      review_id: reviewPayload.review_id,
      energy_level: 2,
      focus_topic: 'Fixed Income',
      max_units: 8,
    },
  });
  expect(session.ok()).toBeTruthy();
  const sessionPayload = await session.json();

  await page.goto(`/review/lab?session=${sessionPayload.session_id}`);

  await expect(page.getByRole('heading', { name: 'Review Lab' })).toBeVisible();
  await expect(page.getByText('Why this today?')).toBeVisible();
  await expect(page.getByPlaceholder('Write your answer before revealing.')).toBeVisible();
  await expect(page.getByText(correctRule)).toHaveCount(0);
  await expect(page.getByText(wrongAnswer)).toHaveCount(0);

  await page.getByPlaceholder('Write your answer before revealing.').fill('effective duration');
  await page.getByRole('button', { name: /Reveal Answer|Reveal Formula/ }).click();

  await expect(page.getByText(correctRule)).toBeVisible();
  await expect(page.getByRole('button', { name: /Forgot/ })).toBeVisible();
  await expect(page.getByRole('button', { name: /Partial/ })).toBeVisible();
  await expect(page.getByRole('button', { name: /Recalled/ })).toBeVisible();
  await expect(page.getByRole('button', { name: /Skip/ })).toBeVisible();
  await expect(page.getByText(wrongAnswer)).toHaveCount(0);
});

test('Review assets import drafts and require confirmation before Review Lab selection', async ({ page }) => {
  const title = 'Playwright CFA note import';
  const note = [
    'Gordon growth model is a dividend discount model for stable perpetual dividend growth.',
    'Intrinsic value = D1 / (r - g).',
    'Use Gordon growth only if dividends grow at a stable rate and required return is greater than growth.',
  ].join('\n');

  await page.goto('/review/assets');
  await expect(page.getByRole('heading', { name: 'Review Assets' })).toBeVisible();
  await expect(page.getByText('Draft assets are not used in normal Review Lab until confirmed.')).toBeVisible();

  await page.getByLabel('Source title').fill(title);
  await page.getByLabel('Note text').fill(note);
  await page.getByRole('button', { name: /Generate candidates/ }).click();

  await expect(page.getByText(/Source ksource-/)).toBeVisible();
  await expect(page.getByText(/draft|needs_review/).first()).toBeVisible();
  await expect(page.getByText(/#seg-/).first()).toBeVisible();

  await clickReviewLabMutation(page, /\/api\/review-lab\/assets\/[^/]+\/confirm$/, page.getByRole('button', { name: /Confirm/ }).first());
  await expect(page.getByText('confirmed').first()).toBeVisible();

  await clickReviewLabMutation(page, /\/api\/review-lab\/assets\/[^/]+\/reject$/, page.getByRole('button', { name: /Reject/ }).nth(1));
  await expect(page.getByText('rejected').first()).toBeVisible();

  const sourcesResponse = await page.request.get(`${API_BASE}/api/review-lab/sources`);
  expect(sourcesResponse.ok()).toBeTruthy();
  const sourcesPayload = await sourcesResponse.json();
  const source = sourcesPayload.sources.find((candidate: any) => candidate.title === title);
  expect(source).toBeTruthy();

  const sourceAssetsResponse = await page.request.get(`${API_BASE}/api/review-lab/assets?source_id=${source.source_id}`);
  expect(sourceAssetsResponse.ok()).toBeTruthy();
  const sourceAssetsPayload = await sourceAssetsResponse.json();
  const confirmedAsset = sourceAssetsPayload.assets.find((asset: any) => asset.validation_status === 'confirmed');
  const rejectedAsset = sourceAssetsPayload.assets.find((asset: any) => asset.validation_status === 'rejected');
  const draftAssetIds = new Set(
    sourceAssetsPayload.assets
      .filter((asset: any) => asset.validation_status === 'draft' || asset.validation_status === 'needs_review')
      .map((asset: any) => asset.asset_id),
  );
  expect(confirmedAsset).toBeTruthy();
  expect(rejectedAsset).toBeTruthy();

  const session = await page.request.post(`${API_BASE}/api/review-lab/generate`, {
    data: {
      review_id: '',
      energy_level: 2,
      focus_topic: 'Review Assets',
      max_units: 10,
    },
  });
  expect(session.ok()).toBeTruthy();
  const sessionPayload = await session.json();
  const unitAssetIds = new Set(sessionPayload.units.map((unit: any) => unit.asset_id));
  expect(unitAssetIds.has(confirmedAsset.asset_id)).toBeTruthy();
  expect(unitAssetIds.has(rejectedAsset.asset_id)).toBeFalsy();
  for (const assetId of draftAssetIds) {
    expect(unitAssetIds.has(assetId)).toBeFalsy();
  }
  const confirmedUnitIndex = sessionPayload.units.findIndex((unit: any) => unit.asset_id === confirmedAsset.asset_id);
  expect(confirmedUnitIndex).toBeGreaterThanOrEqual(0);

  await page.goto(`/review/lab?session=${sessionPayload.session_id}`);
  await expect(page.getByRole('heading', { name: 'Review Lab' })).toBeVisible();
  for (let index = 0; index < confirmedUnitIndex; index += 1) {
    await page.getByRole('button', { name: /Reveal Answer|Reveal Formula/ }).click();
    await page.getByRole('button', { name: /Skip/ }).click();
  }
  await expect(page.getByText(/Gordon growth|Intrinsic value|stable perpetual/)).toBeVisible();
});

test('File uploads feed Review Assets ResourceOS and Dictionary Kernel', async ({ page }, testInfo) => {
  const assetFile = testInfo.outputPath('asset-upload.txt');
  writeFileSync(assetFile, [
    '# Uploaded Asset WACC',
    'LOS: CI-UPLOAD-ASSET',
    'WACC = w_d r_d (1 - t) + w_e r_e.',
    'Use WACC when valuing a firm with a target capital structure.',
    'Source: Playwright uploaded file.',
  ].join('\n'));

  await page.goto('/review/assets');
  await page.getByLabel('Source title').fill(`Playwright File Asset ${Date.now()}`);
  await page.getByLabel('Source file').setInputFiles(assetFile);
  await page.getByRole('button', { name: /^Import file$/ }).click();
  await expect(page.getByText('asset-upload.txt')).toBeVisible();
  await expect(page.getByText('extracted').first()).toBeVisible();
  await expect(page.getByText(/file:file-/).first()).toBeVisible();
  await expect(page.getByText(/draft|needs_review/).first()).toBeVisible();

  const resourceFile = testInfo.outputPath('resource-upload.txt');
  const resourceTitle = `Playwright File Resource ${Date.now()}`;
  writeFileSync(resourceFile, [
    '# Uploaded Resource WACC',
    'LOS: CI-UPLOAD-RESOURCE',
    'WACC = w_d r_d (1 - t) + w_e r_e.',
    'Use when valuing a firm with target capital structure.',
    'Source: Playwright uploaded resource.',
  ].join('\n'));

  await page.goto('/review/resources');
  await page.getByLabel('Resource title').fill(resourceTitle);
  await page.getByLabel('Resource type').selectOption('lecture_slide');
  await page.getByLabel('Resource file').setInputFiles(resourceFile);
  await page.getByRole('button', { name: /^Import file$/ }).click();
  await expect(page.getByText('resource-upload.txt')).toBeVisible();
  await expect(page.getByText(resourceTitle).first()).toBeVisible();
  await expect(page.getByText(/file:file-/).first()).toBeVisible();
  await expect(page.getByText(/draft|needs_review/).first()).toBeVisible();

  const dictionaryFile = testInfo.outputPath('dictionary-upload.json');
  const dictionaryTitle = `Playwright File Dictionary ${Date.now()}`;
  writeFileSync(dictionaryFile, JSON.stringify([
    {
      headword: 'claro',
      language: 'es',
      target_language: 'en',
      part_of_speech: 'adjective',
      definition: 'clear or obvious',
      translation: 'clear',
      example_sentence: 'El mensaje es claro.',
    },
  ]));

  await page.goto('/language/dictionaries');
  await page.getByLabel('Dictionary title').fill(dictionaryTitle);
  await page.getByLabel('Dictionary type').selectOption('spanish_english');
  await page.getByLabel('Dictionary file').setInputFiles(dictionaryFile);
  await page.getByRole('button', { name: /^Import file$/ }).click();
  await expect(page.getByText('dictionary-upload.json')).toBeVisible();
  await expect(page.getByText(dictionaryTitle).first()).toBeVisible();
  await expect(page.getByText('claro').first()).toBeVisible();
  await expect(page.getByText(/file:file-/).first()).toBeVisible();
});

test('ResourceOS gates resources before asset promotion into Review Lab', async ({ page }) => {
  const resourceTitle = `Playwright ResourceOS WACC ${Date.now()}`;
  const resourceText = [
    '# ResourceOS WACC',
    'LOS: CI-PLAY-RES',
    'WACC = w_d r_d (1 - t) + w_e r_e.',
    'Use when valuing a firm with a target capital structure.',
    'Source: curriculum reading note.',
  ].join('\n');

  await page.goto('/review/resources');
  await expect(page.getByRole('heading', { name: 'ResourceOS Quality Gate' })).toBeVisible();
  await expect(page.getByText('Low, draft, and rejected resources do not enter normal Review Lab.')).toBeVisible();

  await page.getByLabel('Resource title').fill(resourceTitle);
  await page.getByLabel('Resource type').selectOption('lecture_slide');
  await page.getByLabel('Resource text').fill(resourceText);
  await page.getByRole('button', { name: /Import resource/ }).click();

  await expect(page.getByText(resourceTitle).first()).toBeVisible();
  await page.getByRole('button', { name: /Score resource/ }).click();
  await expect(page.getByText(/medium|high|trusted/).first()).toBeVisible();

  await page.getByRole('button', { name: /Extract evidence/ }).click();
  await expect(page.getByText(/#seg-/).first()).toBeVisible();
  await expect(page.getByText(/draft|needs_review/).first()).toBeVisible();
  await expect(page.getByText(/source_ref_shared/).first()).toBeVisible();

  const resources = await page.request.get(`${API_BASE}/api/review-lab/resources`);
  expect(resources.ok()).toBeTruthy();
  const resourcePayload = await resources.json();
  const resource = resourcePayload.resources.find((item: any) => item.title === resourceTitle);
  expect(resource).toBeTruthy();

  const candidatesBefore = await page.request.get(`${API_BASE}/api/review-lab/resources/${resource.resource_id}/candidate-assets`);
  expect(candidatesBefore.ok()).toBeTruthy();
  const candidatePayload = await candidatesBefore.json();
  const candidateIds = new Set(candidatePayload.assets.map((asset: any) => asset.asset_id));
  expect(candidateIds.size).toBeGreaterThan(0);

  const reviewBefore = await page.request.post(`${API_BASE}/api/review-lab/generate`, {
    data: { review_id: '', energy_level: 2, max_units: 50 },
  });
  expect(reviewBefore.ok()).toBeTruthy();
  const reviewBeforePayload = await reviewBefore.json();
  expect(reviewBeforePayload.units.some((unit: any) => candidateIds.has(unit.asset_id))).toBeFalsy();

  await page.getByRole('button', { name: /Confirm resource/ }).click();
  await expect(page.getByText('confirmed').first()).toBeVisible();
  await page.getByRole('button', { name: /Promote assets/ }).click();

  const candidatesAfter = await page.request.get(`${API_BASE}/api/review-lab/resources/${resource.resource_id}/candidate-assets`);
  expect(candidatesAfter.ok()).toBeTruthy();
  const promotedPayload = await candidatesAfter.json();
  const promotedAsset = promotedPayload.assets.find((asset: any) => asset.validation_status === 'confirmed');
  expect(promotedAsset).toBeTruthy();

  const reviewAfter = await page.request.post(`${API_BASE}/api/review-lab/generate`, {
    data: { review_id: '', energy_level: 2, max_units: 50 },
  });
  expect(reviewAfter.ok()).toBeTruthy();
  const reviewAfterPayload = await reviewAfter.json();
  expect(reviewAfterPayload.units.some((unit: any) => unit.asset_id === promotedAsset.asset_id)).toBeTruthy();

  await page.getByRole('link', { name: /Coverage/ }).click();
  await expect(page).toHaveURL(/\/review\/coverage/);
  await expect(page.getByRole('heading', { name: 'Coverage Audit' })).toBeVisible();

  const rejectedImport = await page.request.post(`${API_BASE}/api/review-lab/resources/import-text`, {
    data: {
      title: `Rejected ResourceOS Duration ${Date.now()}`,
      text: [
        'Effective duration = (PV- - PV+) / (2 x Delta curve x PV0).',
        'Use effective duration when cash flows can change.',
        'Source: local rejected resource.',
      ].join('\n'),
    },
  });
  expect(rejectedImport.ok()).toBeTruthy();
  const rejectedResource = (await rejectedImport.json()).resource;
  await page.request.post(`${API_BASE}/api/review-lab/resources/${rejectedResource.resource_id}/confirm`);
  const rejectedExtract = await page.request.post(`${API_BASE}/api/review-lab/resources/${rejectedResource.resource_id}/extract-evidence`);
  expect(rejectedExtract.ok()).toBeTruthy();
  const rejectedCandidate = (await rejectedExtract.json()).candidate_assets[0];
  await page.request.post(`${API_BASE}/api/review-lab/resources/${rejectedResource.resource_id}/promote-assets`, {
    data: { asset_ids: [rejectedCandidate.asset_id] },
  });
  await page.request.post(`${API_BASE}/api/review-lab/resources/${rejectedResource.resource_id}/reject`);

  const reviewAfterReject = await page.request.post(`${API_BASE}/api/review-lab/generate`, {
    data: { review_id: '', energy_level: 2, max_units: 50 },
  });
  expect(reviewAfterReject.ok()).toBeTruthy();
  const rejectPayload = await reviewAfterReject.json();
  expect(rejectPayload.units.some((unit: any) => unit.asset_id === rejectedCandidate.asset_id)).toBeFalsy();
});

test('Mission Control summarizes subsystems and links without wrong-answer leakage', async ({ page }) => {
  const wrongPhrase = `UNIQUE_WRONG_MISSION_PLAYWRIGHT_${Date.now()}`;
  const attempt = await page.request.post(`${API_BASE}/api/attempts`, {
    data: {
      topic: 'Corporate Issuers',
      los: 'CI.Mission',
      prompt_or_question: 'Which debt cost belongs in WACC?',
      wrong_choice_or_output: wrongPhrase,
      correct_resolution: 'Use after-tax cost of debt in WACC.',
      error_type: 'concept_confusion',
      confidence: 1,
      time_spent: 75,
      evidence_refs: ['mission-control-e2e'],
      is_correct: false,
    },
  });
  expect(attempt.ok()).toBeTruthy();

  await page.goto('/review/mission-control');
  await expect(page.getByRole('heading', { name: 'Mission Control' })).toBeVisible();
  await expect(page.getByText('Review Today').first()).toBeVisible();
  await expect(page.getByText('Coverage Gaps').first()).toBeVisible();
  await expect(page.getByText('Language Review').first()).toBeVisible();
  await expect(page.getByText('Tutor').first()).toBeVisible();
  await expect(page.getByText('Top Recommendations')).toBeVisible();
  await expect(page.getByText('Advanced diagnostics')).toBeVisible();
  await expect(page.getByText('Route Registry')).toHaveCount(0);
  await expect(page.getByText(wrongPhrase)).toHaveCount(0);

  await page.getByRole('link', { name: /^Review Lab$/ }).click();
  await expect(page).toHaveURL(/\/review\/lab/);
  await page.goto('/review/mission-control');
  await page.getByRole('link', { name: /^Dictionaries$/ }).click();
  await expect(page).toHaveURL(/\/language\/dictionaries/);
  await page.goto('/review/mission-control');
  await page.getByRole('button', { name: /Advanced diagnostics/ }).click();
  await expect(page.getByText('Route Registry')).toBeVisible();
});

test('Study Planner generates energy-aware plans and orchestrates blocks', async ({ page }, testInfo) => {
  const wrongPhrase = `UNIQUE_WRONG_STUDY_PLANNER_PLAYWRIGHT_${Date.now()}`;
  const attempt = await page.request.post(`${API_BASE}/api/attempts`, {
    data: {
      topic: 'Corporate Issuers',
      los: 'CI.Planner',
      prompt_or_question: 'Which debt cost belongs in WACC?',
      wrong_choice_or_output: wrongPhrase,
      correct_resolution: 'Use after-tax cost of debt in WACC.',
      error_type: 'concept_confusion',
      confidence: 1,
      time_spent: 75,
      evidence_refs: ['study-planner-e2e'],
      is_correct: false,
    },
  });
  expect(attempt.ok()).toBeTruthy();
  await page.request.get(`${API_BASE}/api/daily-review/today`);

  await page.request.post(`${API_BASE}/api/review-lab/syllabus/seed-demo`);
  const formula = await page.request.post(`${API_BASE}/api/review-lab/formulas/import-text`, {
    data: {
      title: `Study Planner Formula ${Date.now()}`,
      text: [
        'WACC = w_d r_d (1 - t) + w_e r_e.',
        'Use after-tax cost of debt with target market value weights.',
        'BA II Plus: enter cash flows, set I/Y to WACC, then CPT NPV.',
      ].join('\n'),
    },
  });
  expect(formula.ok()).toBeTruthy();
  const formulaPayload = await formula.json();
  const formulaAsset = formulaPayload.assets.find((asset: any) => asset.asset_type === 'formula');
  expect(formulaAsset).toBeTruthy();
  await page.request.post(`${API_BASE}/api/review-lab/formulas/${formulaAsset.asset_id}/confirm`);

  const draftSource = await page.request.post(`${API_BASE}/api/review-lab/sources/import-text`, {
    data: {
      title: `Study Planner Draft Asset ${Date.now()}`,
      text: [
        'LOS: CI-PLAN-PW-DRAFT',
        'WACC = w_d r_d (1 - t) + w_e r_e.',
        'Use WACC when valuing a firm with target capital structure.',
      ].join('\n'),
      source_type: 'text_note',
    },
  });
  expect(draftSource.ok()).toBeTruthy();
  await page.request.post(`${API_BASE}/api/review-lab/sources/${(await draftSource.json()).source.source_id}/extract-assets`);

  const retro = await page.request.post(`${API_BASE}/api/review-lab/mock-retro/import-text`, {
    data: {
      title: `Study Planner Retro ${Date.now()}`,
      text: [
        'Q1 Corporate Issuers WACC',
        'LOS: CI-PLAN-PW-MOCK',
        'Result: incorrect',
        'Confidence: high',
        `Wrong Output: ${wrongPhrase}`,
        'Correct Rule: WACC uses after-tax cost of debt.',
        'Tested Formula: WACC',
      ].join('\n'),
    },
  });
  expect(retro.ok()).toBeTruthy();
  await page.request.post(`${API_BASE}/api/review-lab/mock-retro/sessions/${(await retro.json()).session.mock_id}/analyze`);

  const dictionary = await page.request.post(`${API_BASE}/api/language-os/dictionaries/import-json`, {
    data: {
      title: `Study Planner Dictionary ${Date.now()}`,
      dictionary_type: 'spanish_english',
      entries: [
        {
          headword: 'repasar',
          language: 'es',
          target_language: 'en',
          part_of_speech: 'verb',
          definition: 'to review or go over again',
          translation: 'review',
          example_sentence: 'Voy a repasar la formula.',
        },
      ],
    },
  });
  expect(dictionary.ok()).toBeTruthy();
  const dictionaryPayload = await dictionary.json();
  const analyticsLexicalId = dictionaryPayload.lexical_assets[0].lexical_id;
  await page.request.post(`${API_BASE}/api/language-os/dictionaries/${dictionaryPayload.dictionary.dictionary_id}/confirm`);
  await page.request.post(`${API_BASE}/api/language-os/lexical-assets/${analyticsLexicalId}/confirm`);

  const unsupportedFile = testInfo.outputPath('study-planner.unsupported');
  writeFileSync(unsupportedFile, 'unsupported planner file');
  await page.goto('/review/assets');
  await page.getByLabel('Source title').fill(`Study Planner Unsupported ${Date.now()}`);
  await page.getByLabel('Source file').setInputFiles(unsupportedFile);
  await page.getByRole('button', { name: /^Import file$/ }).click();
  await expect(page.getByText('unsupported').first()).toBeVisible();

  await page.goto('/review/study-planner');
  await expect(page.getByRole('heading', { name: 'Study Planner' })).toBeVisible();
  await page.getByLabel('Goal').fill('WACC transfer lexical');
  await page.getByLabel('Minutes').fill('90');
  await page.getByRole('button', { name: /Generate plan/ }).click();

  await expect(page.getByText('Plan Minutes')).toBeVisible();
  await expect(page.getByText('Review Lab').first()).toBeVisible();
  await expect(page.getByText('Formula Lab').first()).toBeVisible();
  await expect(page.getByText('Coverage').first()).toBeVisible();
  await expect(page.getByText('Mock Transfer').first()).toBeVisible();
  await expect(page.getByText('Lexical').first()).toBeVisible();
  await expect(page.getByText(/not used as review content/).first()).toBeVisible();
  await expect(page.getByText(wrongPhrase)).toHaveCount(0);

  const firstBlock = page.locator('article').first();
  await firstBlock.getByRole('button', { name: /^Start$/ }).click();
  await expect(firstBlock.getByText('in_progress', { exact: true })).toBeVisible();
  await firstBlock.getByRole('button', { name: /^Complete$/ }).click();
  await expect(firstBlock.getByText('completed', { exact: true })).toBeVisible();

  await page.locator('article').filter({ hasText: 'pending' }).getByRole('button', { name: /^Skip$/ }).first().click();
  await expect(page.getByText('skipped', { exact: true }).first()).toBeVisible();

  await page.getByRole('link', { name: /^Open subsystem$/ }).first().click();
  await expect(page).toHaveURL(/\/review\/lab|\/review\/formulas|\/review\/coverage|\/review\/mock-retro|\/review\/assets|\/review\/resources|\/language\/review|\/language\/dictionaries|\/review\/mission-control/);

  await page.goto('/review/study-planner');
  await page.getByRole('button', { name: /^Low$/ }).click();
  await page.getByRole('button', { name: /Generate plan/ }).click();
  await expect(page.getByText('40/40')).toBeVisible();
  const lowBlockCount = await page.locator('article').count();

  await page.getByRole('button', { name: /^High$/ }).click();
  await page.getByRole('button', { name: /Generate plan/ }).click();
  await expect(page.getByText(/1[4-5][0-9]\/150/)).toBeVisible();
  const highBlockCount = await page.locator('article').count();
  expect(highBlockCount).toBeGreaterThanOrEqual(lowBlockCount);
  await expect(page.getByText('File Cleanup').first()).toBeVisible();

  await page.getByRole('button', { name: /^Complete plan$/ }).click();
  await expect(page.getByText('completed').first()).toBeVisible();
  await expect(page.getByText(wrongPhrase)).toHaveCount(0);
});

test('Learning Analytics aggregates outcomes and keeps correct-only views', async ({ page }) => {
  const wrongPhrase = `UNIQUE_WRONG_ANALYTICS_PLAYWRIGHT_${Date.now()}`;
  const attempt = await page.request.post(`${API_BASE}/api/attempts`, {
    data: {
      topic: 'Corporate Issuers',
      los: 'CI.Analytics',
      prompt_or_question: 'Which debt cost belongs in WACC?',
      wrong_choice_or_output: wrongPhrase,
      correct_resolution: 'Use after-tax cost of debt in WACC.',
      error_type: 'concept_confusion',
      confidence: 4,
      time_spent: 75,
      evidence_refs: ['learning-analytics-e2e'],
      is_correct: false,
    },
  });
  expect(attempt.ok()).toBeTruthy();

  const reviewSource = await page.request.post(`${API_BASE}/api/review-lab/sources/import-text`, {
    data: {
      title: `Analytics Review Source ${Date.now()}`,
      text: [
        'LOS: CI-ANALYTICS-REVIEW',
        'Use after-tax cost of debt in WACC.',
        'Apply target capital weights when valuing the firm.',
      ].join('\n'),
      source_type: 'text_note',
    },
  });
  expect(reviewSource.ok()).toBeTruthy();
  const reviewSourcePayload = await reviewSource.json();
  const extractedReviewAssets = await page.request.post(`${API_BASE}/api/review-lab/sources/${reviewSourcePayload.source.source_id}/extract-assets`);
  expect(extractedReviewAssets.ok()).toBeTruthy();
  const reviewAsset = (await extractedReviewAssets.json()).assets[0];
  expect(reviewAsset).toBeTruthy();
  await page.request.post(`${API_BASE}/api/review-lab/assets/${reviewAsset.asset_id}/confirm`);
  const reviewSession = await page.request.post(`${API_BASE}/api/review-lab/generate`, {
    data: { review_id: '', energy_level: 2, max_units: 4 },
  });
  expect(reviewSession.ok()).toBeTruthy();
  const reviewSessionPayload = await reviewSession.json();
  const reviewUnit = reviewSessionPayload.units[0];
  expect(reviewUnit).toBeTruthy();
  const reviewOutcome = await page.request.post(`${API_BASE}/api/review-lab/sessions/${reviewSessionPayload.session_id}/units/${reviewUnit.unit_id}/outcome`, {
    data: {
      confidence_before: 4,
      time_spent_seconds: 30,
      needed_hint: false,
      outcome: 'forgot',
      confidence_after: 1,
      answer_quality: 'blank',
      next_action: 'drill',
    },
  });
  expect(reviewOutcome.ok()).toBeTruthy();

  await page.request.post(`${API_BASE}/api/review-lab/syllabus/seed-demo`);
  const formula = await page.request.post(`${API_BASE}/api/review-lab/formulas/import-text`, {
    data: {
      title: `Analytics Formula ${Date.now()}`,
      text: [
        'WACC = w_d r_d (1 - t) + w_e r_e.',
        'Use after-tax cost of debt with target capital structure.',
        'BA II Plus: enter cash flows, set I/Y to WACC, then CPT NPV.',
      ].join('\n'),
    },
  });
  expect(formula.ok()).toBeTruthy();
  const formulaAsset = (await formula.json()).assets.find((asset: any) => asset.asset_type === 'formula');
  expect(formulaAsset).toBeTruthy();
  const analyticsFormulaAssetId = formulaAsset.asset_id;
  await page.request.post(`${API_BASE}/api/review-lab/formulas/${analyticsFormulaAssetId}/confirm`);
  const formulaSession = await page.request.post(`${API_BASE}/api/review-lab/formulas/generate-session`, {
    data: { max_units: 4 },
  });
  expect(formulaSession.ok()).toBeTruthy();
  const formulaSessionPayload = await formulaSession.json();
  const formulaUnit = formulaSessionPayload.units[0];
  expect(formulaUnit).toBeTruthy();
  const formulaOutcome = await page.request.post(`${API_BASE}/api/review-lab/formulas/units/${formulaUnit.unit_id}/complete`, {
    data: {
      session_id: formulaSessionPayload.session_id,
      confidence_before: 3,
      time_spent_seconds: 40,
      needed_hint: true,
      outcome: 'partial',
      confidence_after: 2,
      answer_quality: 'minor_gap',
      next_action: 'drill',
    },
  });
  expect(formulaOutcome.ok()).toBeTruthy();

  const dictionary = await page.request.post(`${API_BASE}/api/language-os/dictionaries/import-json`, {
    data: {
      title: `Analytics Dictionary ${Date.now()}`,
      dictionary_type: 'spanish_english',
      entries: [
        {
          headword: 'repasar',
          language: 'es',
          target_language: 'en',
          part_of_speech: 'verb',
          definition: 'to review or go over again',
          translation: 'review',
          example_sentence: 'Voy a repasar la formula.',
          collocations: ['repasar una formula'],
        },
      ],
    },
  });
  expect(dictionary.ok()).toBeTruthy();
  const dictionaryPayload = await dictionary.json();
  const analyticsLexicalId = dictionaryPayload.lexical_assets[0].lexical_id;
  await page.request.post(`${API_BASE}/api/language-os/dictionaries/${dictionaryPayload.dictionary.dictionary_id}/confirm`);
  await page.request.post(`${API_BASE}/api/language-os/lexical-assets/${analyticsLexicalId}/confirm`);
  const lexicalSession = await page.request.post(`${API_BASE}/api/language-os/review/generate-session`, {
    data: { max_units: 4 },
  });
  expect(lexicalSession.ok()).toBeTruthy();
  const lexicalSessionPayload = await lexicalSession.json();
  const lexicalUnit = lexicalSessionPayload.units[0];
  expect(lexicalUnit).toBeTruthy();
  await page.request.post(`${API_BASE}/api/language-os/review/units/${lexicalUnit.unit_id}/complete`, {
    data: { session_id: lexicalSessionPayload.session_id, outcome: 'forgot', time_spent_seconds: 20 },
  });

  const retro = await page.request.post(`${API_BASE}/api/review-lab/mock-retro/import-text`, {
    data: {
      title: `Analytics Retro ${Date.now()}`,
      text: [
        'Q1 Corporate Issuers WACC',
        'LOS: CI-ANALYTICS-PW',
        'Result: incorrect',
        'Confidence: high',
        `Wrong Output: ${wrongPhrase}`,
        'Correct Rule: WACC uses after-tax cost of debt.',
        'Tested Formula: WACC',
      ].join('\n'),
    },
  });
  expect(retro.ok()).toBeTruthy();
  await page.request.post(`${API_BASE}/api/review-lab/mock-retro/sessions/${(await retro.json()).session.mock_id}/analyze`);

  const resource = await page.request.post(`${API_BASE}/api/review-lab/resources/import-text`, {
    data: {
      title: `Analytics Resource ${Date.now()}`,
      resource_type: 'lecture_slide',
      text: [
        'LOS: CI-ANALYTICS-RESOURCE',
        'WACC = w_d r_d (1 - t) + w_e r_e.',
        'Use after-tax cost of debt with target capital structure.',
        'Source: curriculum reading note.',
      ].join('\n'),
    },
  });
  expect(resource.ok()).toBeTruthy();
  const resourceId = (await resource.json()).resource.resource_id;
  await page.request.post(`${API_BASE}/api/review-lab/resources/${resourceId}/score`);
  await page.request.post(`${API_BASE}/api/review-lab/resources/${resourceId}/confirm`);
  await page.request.post(`${API_BASE}/api/review-lab/resources/${resourceId}/extract-evidence`);
  const promoted = await page.request.post(`${API_BASE}/api/review-lab/resources/${resourceId}/promote-assets`, { data: { asset_ids: [] } });
  expect(promoted.ok()).toBeTruthy();
  const analyticsPromotedAssetIds = ((await promoted.json()).assets || []).map((asset: any) => asset.asset_id);

  const plan = await page.request.post(`${API_BASE}/api/study-planner/generate`, {
    data: { energy_mode: 'normal', available_minutes: 90, goal: 'analytics WACC' },
  });
  expect(plan.ok()).toBeTruthy();
  const planPayload = await plan.json();
  const firstPending = planPayload.blocks.find((block: any) => block.status === 'pending');
  expect(firstPending).toBeTruthy();
  await page.request.post(`${API_BASE}/api/study-planner/blocks/${firstPending.block_id}/start`);
  await page.request.post(`${API_BASE}/api/study-planner/blocks/${firstPending.block_id}/complete`, {
    data: { outcome: 'analytics completed block', actual_minutes: firstPending.target_minutes },
  });
  await page.request.post(`${API_BASE}/api/study-planner/plans/${planPayload.plan_id}/complete`);
  await page.request.post(`${API_BASE}/api/review-lab/syllabus/recompute-coverage`);
  const recompute = await page.request.post(`${API_BASE}/api/learning-analytics/recompute`, {
    data: { profile_id: 'default', range: '30d' },
  });
  expect(recompute.ok()).toBeTruthy();

  await page.goto('/review/analytics');
  await expect(page.getByRole('heading', { name: 'Learning Analytics' })).toBeVisible();
  await expect(page.getByText('Mastery Trend', { exact: true })).toBeVisible();
  await expect(page.getByText('Confidence Calibration')).toBeVisible();
  await expect(page.getByText('Plan Adherence')).toBeVisible();
  await expect(page.getByText('Coverage Momentum')).toBeVisible();
  await expect(page.getByText('Formula Weakness').first()).toBeVisible();
  await expect(page.getByText('Language Production Gap')).toBeVisible();
  await expect(page.getByText('Resource Usefulness').first()).toBeVisible();
  await expect(page.getByText('Recommended Strategy Adjustments')).toBeVisible();
  await expect(page.getByText('Topic Mastery Trends')).toBeVisible();
  await expect(page.getByText('Plan Block Completion')).toBeVisible();
  await expect(page.getByText('Transfer Gap Trend')).toBeVisible();
  await expect(page.getByText('Lexical Weakness')).toBeVisible();
  await expect(page.getByText('Correct-only analytics')).toBeVisible();
  await expect(page.getByText(wrongPhrase)).toHaveCount(0);

  await page.getByRole('button', { name: /^7 days$/ }).click();
  await expect(page.getByText('Recommended Strategy Adjustments')).toBeVisible();
  await expect(page.getByText(wrongPhrase)).toHaveCount(0);

  await page.getByRole('link', { name: /^Planner$/ }).click();
  await expect(page).toHaveURL(/\/review\/study-planner/);
  await page.goto('/review/analytics');
  await page.getByRole('link', { name: /^Mission$/ }).first().click();
  await expect(page).toHaveURL(/\/review\/mission-control/);
  await page.request.post(`${API_BASE}/api/language-os/lexical-assets/${analyticsLexicalId}/reject`);
  await page.request.post(`${API_BASE}/api/review-lab/formulas/${analyticsFormulaAssetId}/reject`);
  for (const assetId of analyticsPromotedAssetIds) {
    await page.request.post(`${API_BASE}/api/review-lab/assets/${assetId}/reject`);
  }
});

test('Adaptive Assessments generate interleaved correct-only drills and feed retro analytics', async ({ page }) => {
  const wrongPhrase = `UNIQUE_WRONG_ASSESSMENT_PLAYWRIGHT_${Date.now()}`;

  const reviewSource = await page.request.post(`${API_BASE}/api/review-lab/sources/import-text`, {
    data: {
      title: `Assessment UI Review Source ${Date.now()}`,
      text: [
        'LOS: CI-ASSESS-PW-REVIEW',
        'Use after-tax cost of debt in WACC.',
        'Apply target capital weights when valuing the firm.',
      ].join('\n'),
      source_type: 'text_note',
    },
  });
  expect(reviewSource.ok()).toBeTruthy();
  const reviewSourcePayload = await reviewSource.json();
  const extractedReviewAssets = await page.request.post(`${API_BASE}/api/review-lab/sources/${reviewSourcePayload.source.source_id}/extract-assets`);
  expect(extractedReviewAssets.ok()).toBeTruthy();
  const reviewAssets = (await extractedReviewAssets.json()).assets;
  expect(reviewAssets.length).toBeGreaterThan(0);
  await page.request.post(`${API_BASE}/api/review-lab/assets/${reviewAssets[0].asset_id}/confirm`);

  const formula = await page.request.post(`${API_BASE}/api/review-lab/formulas/import-text`, {
    data: {
      title: `Assessment UI Formula ${Date.now()}`,
      text: [
        'WACC = w_d r_d (1 - t) + w_e r_e.',
        'Use after-tax cost of debt with target market value weights.',
        'BA II Plus: enter cash flows, set I/Y to WACC, then CPT NPV.',
      ].join('\n'),
    },
  });
  expect(formula.ok()).toBeTruthy();
  const formulaAsset = (await formula.json()).assets.find((asset: any) => asset.asset_type === 'formula');
  expect(formulaAsset).toBeTruthy();
  await page.request.post(`${API_BASE}/api/review-lab/formulas/${formulaAsset.asset_id}/confirm`);

  const dictionary = await page.request.post(`${API_BASE}/api/language-os/dictionaries/import-json`, {
    data: {
      title: `Assessment UI Dictionary ${Date.now()}`,
      dictionary_type: 'spanish_english',
      entries: [
        {
          headword: 'repasar',
          language: 'es',
          target_language: 'en',
          part_of_speech: 'verb',
          definition: 'to review or go over again',
          translation: 'review',
          example_sentence: 'Voy a repasar la formula.',
          collocations: ['repasar una formula'],
        },
      ],
    },
  });
  expect(dictionary.ok()).toBeTruthy();
  const dictionaryPayload = await dictionary.json();
  await page.request.post(`${API_BASE}/api/language-os/dictionaries/${dictionaryPayload.dictionary.dictionary_id}/confirm`);
  await page.request.post(`${API_BASE}/api/language-os/lexical-assets/${dictionaryPayload.lexical_assets[0].lexical_id}/confirm`);

  const retro = await page.request.post(`${API_BASE}/api/review-lab/mock-retro/import-text`, {
    data: {
      title: `Assessment UI Retro ${Date.now()}`,
      text: [
        'Q1 Corporate Issuers WACC',
        'LOS: CI-ASSESS-PW-MOCK',
        'Result: incorrect',
        'Confidence: high',
        `Wrong Output: ${wrongPhrase}`,
        'Correct Rule: WACC uses after-tax cost of debt.',
        'Tested Formula: WACC',
      ].join('\n'),
    },
  });
  expect(retro.ok()).toBeTruthy();
  await page.request.post(`${API_BASE}/api/review-lab/mock-retro/sessions/${(await retro.json()).session.mock_id}/analyze`);
  await page.request.post(`${API_BASE}/api/review-lab/syllabus/seed-demo`);
  await page.request.post(`${API_BASE}/api/review-lab/syllabus/recompute-coverage`);

  await page.goto('/review/assessments');
  await expect(page.getByRole('heading', { name: 'Adaptive Assessments' })).toBeVisible();
  await expect(page.getByText('Correct-only assessment feedback')).toBeVisible();
  await expect(page.getByRole('link', { name: /^Analytics$/ })).toBeVisible();
  await expect(page.getByRole('link', { name: /^Planner$/ })).toBeVisible();
  await expect(page.getByRole('link', { name: /^Mission$/ })).toBeVisible();
  await expect(page.getByText(wrongPhrase)).toHaveCount(0);

  await clickReviewLabMutation(page, /\/api\/assessments\/generate$/, page.getByRole('button', { name: /Generate assessment/ }));
  await expect(page.getByText('Interleaving Drill').first()).toBeVisible();

  const list = await page.request.get(`${API_BASE}/api/assessments?profile_id=default&limit=1`);
  expect(list.ok()).toBeTruthy();
  const session = (await list.json()).assessments[0];
  expect(session).toBeTruthy();
  const categories = new Set(session.questions.map((question: any) => question.category));
  expect(categories.has('formula')).toBeTruthy();
  expect(categories.has('lexical')).toBeTruthy();
  expect(categories.has('transfer')).toBeTruthy();
  const textQuestionIndex = session.questions.findIndex((question: any) => !question.choices?.length);
  expect(textQuestionIndex).toBeGreaterThanOrEqual(0);

  for (let index = 0; index < textQuestionIndex; index += 1) {
    await page.getByRole('button', { name: /Next question/ }).click();
  }
  const startButton = page.getByRole('button', { name: /^Start$/ });
  if (await startButton.isVisible().catch(() => false)) {
    await startButton.click();
  }

  const answerBox = page.getByPlaceholder('Write your answer before revealing correct feedback.');
  await expect(answerBox).toBeVisible();
  await answerBox.fill(wrongPhrase);
  await expect(page.getByText('Correct Feedback')).toHaveCount(0);
  await page.getByRole('button', { name: /Submit answer/ }).click();
  await expect(page.getByText('Correct Feedback')).toBeVisible();
  await expect(page.getByText('Correct Answer', { exact: true })).toBeVisible();
  await expect(page.getByText('Correct Rule', { exact: true })).toBeVisible();
  await expect(page.getByText('Correct Reasoning', { exact: true })).toBeVisible();
  await expect(page.getByText(wrongPhrase)).toHaveCount(0);

  await page.getByRole('button', { name: /Self-grade partial/ }).click();
  await page.getByRole('button', { name: /Complete assessment/ }).click();
  await expect(page.getByText('Correct Rules To Review')).toBeVisible();
  await expect(page.getByText('Transfer Gaps', { exact: true })).toBeVisible();
  await expect(page.getByText(wrongPhrase)).toHaveCount(0);

  const assessment = await page.request.get(`${API_BASE}/api/assessments/${session.assessment_id}`);
  expect(assessment.ok()).toBeTruthy();
  expect(JSON.stringify(await assessment.json())).not.toContain(wrongPhrase);

  const assessmentRetro = await page.request.get(`${API_BASE}/api/assessments/${session.assessment_id}/retro`);
  expect(assessmentRetro.ok()).toBeTruthy();
  const retroPayload = await assessmentRetro.json();
  expect(retroPayload.transfer_gaps_created).toBeGreaterThanOrEqual(1);
  expect(JSON.stringify(retroPayload)).not.toContain(wrongPhrase);

  const analytics = await page.request.get(`${API_BASE}/api/learning-analytics/events?profile_id=default&range=30d`);
  expect(analytics.ok()).toBeTruthy();
  const analyticsBody = JSON.stringify(await analytics.json());
  expect(analyticsBody).toContain('assessment');
  expect(analyticsBody).not.toContain(wrongPhrase);

  await page.getByRole('link', { name: /^Analytics$/ }).click();
  await expect(page).toHaveURL(/\/review\/analytics/);
  await expect(page.getByRole('link', { name: /^Assessments\b/ })).toBeVisible();

  await page.goto('/review/study-planner');
  await expect(page.getByRole('link', { name: /^Assessments$/ })).toBeVisible();
  await page.getByRole('link', { name: /^Assessments$/ }).click();
  await expect(page).toHaveURL(/\/review\/assessments/);

  await page.goto('/review/mission-control');
  await expect(page.getByRole('link', { name: /More Tools/ })).toBeVisible();
  await page.getByRole('link', { name: /More Tools/ }).click();
  await expect(page).toHaveURL(/\/review\/tools/);
  await expect(page.getByRole('link', { name: /^Assessments\b/ })).toBeVisible();
});

test('Knowledge Graph search traces learning objects without wrong-answer leakage', async ({ page }) => {
  const stamp = Date.now();
  const traceToken = `KGTRACE-${stamp}`;
  const wrongPhrase = `UNIQUE_WRONG_GRAPH_PLAYWRIGHT_${stamp}`;

  const reviewSource = await page.request.post(`${API_BASE}/api/review-lab/sources/import-text`, {
    data: {
      title: `Knowledge Graph Review Source ${traceToken}`,
      text: [
        `LOS: CI-GRAPH-PW-${stamp}`,
        `${traceToken} WACC requires after-tax cost of debt.`,
        'Target capital weights belong in WACC.',
      ].join('\n'),
      source_type: 'text_note',
    },
  });
  expect(reviewSource.ok()).toBeTruthy();
  const sourcePayload = await reviewSource.json();
  const extracted = await page.request.post(`${API_BASE}/api/review-lab/sources/${sourcePayload.source.source_id}/extract-assets`);
  expect(extracted.ok()).toBeTruthy();
  const reviewAsset = (await extracted.json()).assets[0];
  expect(reviewAsset).toBeTruthy();
  await page.request.post(`${API_BASE}/api/review-lab/assets/${reviewAsset.asset_id}/confirm`);

  const resource = await page.request.post(`${API_BASE}/api/review-lab/resources/import-text`, {
    data: {
      title: `Knowledge Graph Resource ${traceToken}`,
      resource_type: 'lecture_slide',
      text: [
        `LOS: CI-GRAPH-RESOURCE-${stamp}`,
        `${traceToken} WACC = w_d r_d (1 - t) + w_e r_e.`,
        'Use after-tax cost of debt with target capital structure.',
      ].join('\n'),
    },
  });
  expect(resource.ok()).toBeTruthy();
  const resourceId = (await resource.json()).resource.resource_id;
  await page.request.post(`${API_BASE}/api/review-lab/resources/${resourceId}/score`);
  await page.request.post(`${API_BASE}/api/review-lab/resources/${resourceId}/confirm`);
  await page.request.post(`${API_BASE}/api/review-lab/resources/${resourceId}/extract-evidence`);
  await page.request.post(`${API_BASE}/api/review-lab/resources/${resourceId}/promote-assets`, { data: { asset_ids: [] } });

  const formula = await page.request.post(`${API_BASE}/api/review-lab/formulas/import-text`, {
    data: {
      title: `Knowledge Graph WACC Formula ${traceToken}`,
      text: [
        `${traceToken} WACC = w_d r_d (1 - t) + w_e r_e.`,
        'Use after-tax cost of debt with target market value weights.',
        'BA II Plus: enter cash flows, set I/Y to WACC, then CPT NPV.',
      ].join('\n'),
    },
  });
  expect(formula.ok()).toBeTruthy();
  const formulaAsset = (await formula.json()).assets.find((asset: any) => asset.asset_type === 'formula');
  expect(formulaAsset).toBeTruthy();
  await page.request.post(`${API_BASE}/api/review-lab/formulas/${formulaAsset.asset_id}/confirm`);

  const dictionary = await page.request.post(`${API_BASE}/api/language-os/dictionaries/import-json`, {
    data: {
      title: `Knowledge Graph Dictionary ${traceToken}`,
      dictionary_type: 'spanish_english',
      entries: [
        {
          headword: 'repasar',
          language: 'es',
          target_language: 'en',
          part_of_speech: 'verb',
          definition: `to review ${traceToken} again`,
          translation: 'review',
          example_sentence: 'Voy a repasar la formula.',
          collocations: ['repasar una formula'],
        },
      ],
    },
  });
  expect(dictionary.ok()).toBeTruthy();
  const dictionaryPayload = await dictionary.json();
  await page.request.post(`${API_BASE}/api/language-os/dictionaries/${dictionaryPayload.dictionary.dictionary_id}/confirm`);
  await page.request.post(`${API_BASE}/api/language-os/lexical-assets/${dictionaryPayload.lexical_assets[0].lexical_id}/confirm`);

  const retro = await page.request.post(`${API_BASE}/api/review-lab/mock-retro/import-text`, {
    data: {
      title: `Knowledge Graph Mock Retro ${traceToken}`,
      text: [
        `Q1 Corporate Issuers WACC ${traceToken}`,
        `LOS: CI-GRAPH-MOCK-${stamp}`,
        'Result: incorrect',
        'Confidence: high',
        `Wrong Output: ${wrongPhrase}`,
        'Correct Rule: WACC uses after-tax cost of debt.',
        'Tested Formula: WACC',
      ].join('\n'),
    },
  });
  expect(retro.ok()).toBeTruthy();
  await page.request.post(`${API_BASE}/api/review-lab/mock-retro/sessions/${(await retro.json()).session.mock_id}/analyze`);
  await page.request.post(`${API_BASE}/api/review-lab/syllabus/seed-demo`);
  await page.request.post(`${API_BASE}/api/review-lab/syllabus/recompute-coverage`);

  const assessment = await page.request.post(`${API_BASE}/api/assessments/generate`, {
    data: { mode: 'formula_drill', target_minutes: 20, question_count: 4, focus: 'formula' },
  });
  expect(assessment.ok()).toBeTruthy();
  const assessmentSession = await assessment.json();
  const formulaQuestion = assessmentSession.questions.find((question: any) => ['formula_setup', 'calculator_steps'].includes(question.question_type));
  expect(formulaQuestion).toBeTruthy();
  await page.request.post(`${API_BASE}/api/assessments/${assessmentSession.assessment_id}/start`);
  await page.request.post(`${API_BASE}/api/assessments/questions/${formulaQuestion.question_id}/answer`, {
    data: { answer_text: wrongPhrase, confidence_before: 0.9, time_spent_seconds: 30 },
  });
  await page.request.post(`${API_BASE}/api/assessments/questions/${formulaQuestion.question_id}/self-grade`, {
    data: { grade: 'partial', confidence_after: 0.4 },
  });
  await page.request.post(`${API_BASE}/api/assessments/${assessmentSession.assessment_id}/complete`);

  const plan = await page.request.post(`${API_BASE}/api/study-planner/generate`, {
    data: { energy_mode: 'normal', available_minutes: 90, goal: `trace ${traceToken}` },
  });
  expect(plan.ok()).toBeTruthy();
  const planPayload = await plan.json();
  const pending = planPayload.blocks.find((block: any) => block.status === 'pending');
  await page.request.post(`${API_BASE}/api/study-planner/blocks/${pending.block_id}/start`);
  await page.request.post(`${API_BASE}/api/study-planner/blocks/${pending.block_id}/complete`, {
    data: { outcome: 'graph trace complete', actual_minutes: pending.target_minutes },
  });
  await page.request.post(`${API_BASE}/api/study-planner/plans/${planPayload.plan_id}/complete`);
  await page.request.post(`${API_BASE}/api/learning-analytics/recompute`, {
    data: { profile_id: 'default', range: '30d' },
  });

  const recompute = await page.request.post(`${API_BASE}/api/knowledge-graph/recompute`, {
    data: { profile_id: 'default' },
  });
  expect(recompute.ok()).toBeTruthy();
  const recomputeBody = await recompute.json();
  expect(recomputeBody.summary.nodes_by_type.formula).toBeGreaterThanOrEqual(1);
  expect(recomputeBody.summary.nodes_by_type.assessment_question).toBeGreaterThanOrEqual(1);
  expect(JSON.stringify(recomputeBody)).not.toContain(wrongPhrase);

  const formulaSearch = await page.request.get(
    `${API_BASE}/api/knowledge-graph/search?profile_id=default&q=${encodeURIComponent(traceToken)}&node_type=formula`,
  );
  expect(formulaSearch.ok()).toBeTruthy();
  const formulaResults = (await formulaSearch.json()).results;
  expect(formulaResults.length).toBeGreaterThan(0);
  const formulaNodeId = formulaResults[0].node.node_id;
  const trace = await page.request.get(`${API_BASE}/api/knowledge-graph/nodes/${formulaNodeId}/trace?profile_id=default`);
  expect(trace.ok()).toBeTruthy();
  const traceBody = await trace.json();
  const connectedTraceTypes = [
    ...traceBody.upstream_lineage,
    ...traceBody.downstream_usage,
    ...traceBody.related_nodes,
  ].map((node: any) => node.node_type);
  expect(connectedTraceTypes.length).toBeGreaterThan(0);
  expect(JSON.stringify(traceBody)).not.toContain(wrongPhrase);
  const assessmentQuestionSearch = await page.request.get(`${API_BASE}/api/knowledge-graph/search?profile_id=default&q=WACC&node_type=assessment_question`);
  expect(assessmentQuestionSearch.ok()).toBeTruthy();
  expect((await assessmentQuestionSearch.json()).results.length).toBeGreaterThan(0);

  await page.goto('/review/search');
  await expect(page.getByRole('heading', { name: 'Global Search' })).toBeVisible();
  await expect(page.getByText('Correct-only graph search')).toBeVisible();
  await page.getByLabel('Query').fill(traceToken);
  await page.getByLabel('Node type').selectOption('formula');
  await page.getByRole('button', { name: /^Apply$/ }).click();
  await expect(page.getByText(traceToken).first()).toBeVisible();
  await expect(page.getByText('Upstream')).toBeVisible();
  await expect(page.getByText('Downstream')).toBeVisible();
  await expect(page.getByText('Impact Analysis')).toBeVisible();
  await expect(page.getByText(wrongPhrase)).toHaveCount(0);

  await page.getByLabel('Query').fill('repasar');
  await page.getByLabel('Node type').selectOption('lexical_asset');
  await page.getByRole('button', { name: /^Apply$/ }).click();
  await expect(page.getByRole('button', { name: /Lexical Asset.*repasar/ }).first()).toBeVisible();
  await expect(page.getByText('repasar').first()).toBeVisible();
  await expect(page.getByText(wrongPhrase)).toHaveCount(0);

  await page.goto('/review/knowledge-map');
  await expect(page.getByRole('heading', { name: 'Knowledge Map' })).toBeVisible();
  await expect(page.getByText('Correct-only traceability map')).toBeVisible();
  await expect(page.getByText('Nodes By Type')).toBeVisible();
  await expect(page.getByText('Edges By Type')).toBeVisible();
  await expect(page.getByText('Impact Analysis')).toBeVisible();
  await expect(page.getByText(wrongPhrase)).toHaveCount(0);
  await page.getByRole('link', { name: /^Global Search$/ }).click();
  await expect(page).toHaveURL(/\/review\/search/);

  await page.goto('/review/mission-control');
  await expect(page.getByRole('link', { name: /More Tools/ })).toBeVisible();
  await page.getByRole('link', { name: /More Tools/ }).click();
  await expect(page).toHaveURL(/\/review\/tools/);
  await expect(page.getByRole('link', { name: /^Search\b/ })).toBeVisible();
  await expect(page.getByRole('link', { name: /^Knowledge Map\b/ })).toBeVisible();
  await page.goto('/review/analytics');
  await expect(page.getByRole('link', { name: /^Search$/ })).toBeVisible();
  await expect(page.getByRole('link', { name: /^Map$/ })).toBeVisible();
  await page.goto('/review/study-planner');
  await expect(page.getByRole('link', { name: /^Search$/ })).toBeVisible();
  await expect(page.getByRole('link', { name: /^Knowledge Map$/ })).toBeVisible();
});

test('TASK-014 keyboard-first review flows remain correct-only', async ({ page }) => {
  const wrongPhrase = `UNIQUE_WRONG_UX_TASK014_${Date.now()}`;

  const attempt = await page.request.post(`${API_BASE}/api/attempts`, {
    data: {
      topic: 'Fixed Income',
      los: 'FI.UX.Keyboard',
      prompt_or_question: 'Which duration measure fits callable bonds?',
      wrong_choice_or_output: wrongPhrase,
      correct_resolution: 'Use effective duration when cash flows can change.',
      error_type: 'concept_confusion',
      confidence: 1,
      time_spent: 60,
      evidence_refs: ['task014-keyboard'],
      is_correct: false,
    },
  });
  expect(attempt.ok()).toBeTruthy();
  const dailyReview = await page.request.get(`${API_BASE}/api/daily-review/today`);
  expect(dailyReview.ok()).toBeTruthy();
  const reviewPayload = await dailyReview.json();
  const reviewSession = await page.request.post(`${API_BASE}/api/review-lab/generate`, {
    data: { review_id: reviewPayload.review_id, energy_level: 2, focus_topic: 'Fixed Income', max_units: 4 },
  });
  expect(reviewSession.ok()).toBeTruthy();
  const reviewSessionPayload = await reviewSession.json();

  await page.goto(`/review/lab?session=${reviewSessionPayload.session_id}`);
  await expect(page.getByRole('heading', { name: 'Review Lab' })).toBeVisible();
  await page.keyboard.press('?');
  await expect(page.getByText('Keyboard shortcuts')).toBeVisible();
  await page.keyboard.press('R');
  await expect(page.getByRole('button', { name: /2 Partial/ })).toBeVisible();
  const reviewOutcomeResponse = page.waitForResponse((response) =>
    response.url().includes(`/api/review-lab/sessions/${reviewSessionPayload.session_id}/units/`) &&
    response.request().method() === 'POST',
  );
  await page.keyboard.press('2');
  await reviewOutcomeResponse;
  await expect(page.getByText(wrongPhrase)).toHaveCount(0);
  await page.request.post(`${API_BASE}/api/review-lab/sessions/${reviewSessionPayload.session_id}/complete`);

  const formula = await page.request.post(`${API_BASE}/api/review-lab/formulas/import-text`, {
    data: {
      title: `TASK014 Keyboard Formula ${Date.now()}`,
      text: [
        'WACC = w_d r_d (1 - t) + w_e r_e.',
        'Use after-tax cost of debt with target market value weights.',
        'BA II Plus: enter cash flows, set I/Y to WACC, then CPT NPV.',
      ].join('\n'),
    },
  });
  expect(formula.ok()).toBeTruthy();
  const formulaAsset = (await formula.json()).assets.find((asset: any) => asset.asset_type === 'formula');
  expect(formulaAsset).toBeTruthy();
  await page.request.post(`${API_BASE}/api/review-lab/formulas/${formulaAsset.asset_id}/confirm`);

  await page.goto('/review/formulas');
  await expect(page.getByRole('heading', { name: 'Formula Lab' })).toBeVisible();
  const formulaSessionResponse = page.waitForResponse((response) =>
    response.url().includes('/api/review-lab/formulas/generate-session') &&
    response.request().method() === 'POST',
  );
  await page.getByRole('button', { name: /Start Formula Lab/ }).click();
  const formulaSessionPayload = await (await formulaSessionResponse).json();
  await expect(page.getByTestId('formula-session-panel')).toBeVisible();
  await page.keyboard.press('?');
  await expect(page.getByText('Keyboard shortcuts')).toBeVisible();
  await page.keyboard.press('R');
  await expect(page.getByTestId('formula-session-panel').getByText('BA II Plus', { exact: true })).toBeVisible();
  const formulaOutcomeResponse = page.waitForResponse((response) =>
    response.url().includes('/api/review-lab/formulas/units/') &&
    response.request().method() === 'POST',
  );
  await page.keyboard.press('2');
  await formulaOutcomeResponse;
  await expect(page.getByText(wrongPhrase)).toHaveCount(0);
  await page.request.post(`${API_BASE}/api/review-lab/sessions/${formulaSessionPayload.session_id}/complete`);

  const dictionary = await page.request.post(`${API_BASE}/api/language-os/dictionaries/import-json`, {
    data: {
      title: `TASK014 Keyboard Dictionary ${Date.now()}`,
      dictionary_type: 'spanish_english',
      entries: [
        {
          headword: 'repasar',
          language: 'es',
          target_language: 'en',
          part_of_speech: 'verb',
          definition: 'to review or go over again',
          translation: 'review',
          example_sentence: 'Voy a repasar la formula.',
          collocations: ['repasar una formula'],
        },
      ],
    },
  });
  expect(dictionary.ok()).toBeTruthy();
  const dictionaryPayload = await dictionary.json();
  await page.request.post(`${API_BASE}/api/language-os/dictionaries/${dictionaryPayload.dictionary.dictionary_id}/confirm`);
  await page.request.post(`${API_BASE}/api/language-os/lexical-assets/${dictionaryPayload.lexical_assets[0].lexical_id}/confirm`);

  await page.goto('/language/review');
  await expect(page.getByRole('heading', { name: 'Lexical Review' })).toBeVisible();
  const lexicalSessionResponse = page.waitForResponse((response) =>
    response.url().includes('/api/language-os/review/generate-session') &&
    response.request().method() === 'POST',
  );
  await page.getByRole('button', { name: /Generate lexical review/ }).click();
  const lexicalSessionPayload = await (await lexicalSessionResponse).json();
  await expect(page.getByText('repasar').first()).toBeVisible();
  await page.keyboard.press('?');
  await expect(page.getByText('Keyboard shortcuts')).toBeVisible();
  await page.keyboard.press('R');
  await expect(page.getByText('Correct answer')).toBeVisible();
  const lexicalOutcomeResponse = page.waitForResponse((response) =>
    response.url().includes('/api/language-os/review/units/') &&
    response.request().method() === 'POST',
  );
  await page.keyboard.press('2');
  await lexicalOutcomeResponse;
  await expect(page.getByText(wrongPhrase)).toHaveCount(0);
  const latestLexicalSession = await page.request.get(`${API_BASE}/api/language-os/review/sessions/${lexicalSessionPayload.session_id}`);
  expect(latestLexicalSession.ok()).toBeTruthy();
  const latestLexicalPayload = await latestLexicalSession.json();
  const completedLexicalUnits = new Set(latestLexicalPayload.completed_unit_ids || []);
  for (const unit of latestLexicalPayload.units || []) {
    if (!completedLexicalUnits.has(unit.unit_id)) {
      await page.request.post(`${API_BASE}/api/language-os/review/units/${unit.unit_id}/complete`, {
        data: { session_id: lexicalSessionPayload.session_id, outcome: 'skipped', time_spent_seconds: 1 },
      });
    }
  }
  await page.request.post(`${API_BASE}/api/language-os/lexical-assets/${dictionaryPayload.lexical_assets[0].lexical_id}/reject`);
  await page.request.post(`${API_BASE}/api/review-lab/formulas/${formulaAsset.asset_id}/reject`);

  await page.goto('/review/assessments');
  await expect(page.getByRole('heading', { name: 'Adaptive Assessments' })).toBeVisible();
  await page.keyboard.press('?');
  await expect(page.getByText('Keyboard shortcuts')).toBeVisible();
});

test('TASK-014 mobile accessibility smoke covers cockpit pages', async ({ page }) => {
  const pages = [
    ['/review/mission-control', 'Mission Control'],
    ['/review/study-planner', 'Study Planner'],
    ['/review/lab', 'Review Lab'],
    ['/review/assessments', 'Adaptive Assessments'],
    ['/review/search', 'Global Search'],
    ['/review/knowledge-map', 'Knowledge Map'],
  ] as const;

  await page.setViewportSize({ width: 390, height: 844 });
  for (const [path, heading] of pages) {
    await page.goto(path);
    await expect(page.getByRole('heading', { name: heading })).toBeVisible();
    const unnamedButtons = await page.locator('button').evaluateAll((buttons) =>
      buttons.filter((button) => !((button.textContent || '').trim() || button.getAttribute('aria-label') || button.getAttribute('title'))).length,
    );
    expect(unnamedButtons).toBe(0);
    const unnamedFields = await page.locator('input, textarea, select').evaluateAll((fields) =>
      fields.filter((field) => {
        if (field.closest('label')) return false;
        const id = field.getAttribute('id');
        const explicitLabel = id ? document.querySelector(`label[for="${id}"]`) : null;
        const label = field.getAttribute('aria-label') || field.getAttribute('title') || field.getAttribute('placeholder') || '';
        return !explicitLabel && !label.trim();
      }).length,
    );
    expect(unnamedFields).toBe(0);
    const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
    const viewportWidth = await page.evaluate(() => window.innerWidth);
    expect(scrollWidth).toBeLessThanOrEqual(viewportWidth + 4);
  }
});

test('TASK-015 data governance exports safe backups and gates restore reset controls', async ({ page }) => {
  const wrongPhrase = `UNIQUE_WRONG_BACKUP_UI_${Date.now()}`;
  const attempt = await page.request.post(`${API_BASE}/api/attempts`, {
    data: {
      topic: 'Fixed Income',
      los: 'FI.DATA.UI',
      prompt_or_question: 'Which duration measure fits callable bonds?',
      wrong_choice_or_output: wrongPhrase,
      correct_resolution: 'Use effective duration when cash flows can change.',
      error_type: 'concept_confusion',
      confidence: 1,
      time_spent: 45,
      evidence_refs: ['task015-ui'],
      is_correct: false,
    },
  });
  expect(attempt.ok()).toBeTruthy();

  await page.goto('/review/data');
  await expect(page.getByRole('heading', { name: 'Data Governance' })).toBeVisible();
  await expect(page.getByText('Inventory')).toBeVisible();
  await expect(page.getByText('Privacy Report')).toBeVisible();
  await expect(page.getByText(wrongPhrase)).toHaveCount(0);

  await expect(page.getByRole('button', { name: /Create full export/ })).toBeDisabled();
  await page.getByLabel(/Include raw diagnostics/).check();
  await expect(page.getByRole('button', { name: /Create full export/ })).toBeEnabled();
  await page.getByLabel(/Include raw diagnostics/).uncheck();

  await page.getByRole('button', { name: /Create safe export/ }).click();
  await expect(page.getByText(/Export created:/)).toBeVisible();
  const exportMessage = await page.getByText(/Export created:/).textContent();
  expect(exportMessage || '').toContain('.system/memory/backups/');
  await expect(page.getByText(wrongPhrase)).toHaveCount(0);

  await page.getByRole('button', { name: /^Dry run$/ }).click();
  await expect(page.getByText('Dry run valid')).toBeVisible();

  const resetButton = page.getByRole('button', { name: /Reset category/ });
  await expect(resetButton).toBeDisabled();
  await page.getByLabel('Confirmation').fill('RESET');
  await expect(resetButton).toBeDisabled();
  await page.getByLabel('Confirmation').fill('RESET knowledge_graph');
  await expect(resetButton).toBeEnabled();

  await page.getByRole('link', { name: /Mission Control/ }).first().click();
  await expect(page).toHaveURL(/\/review\/mission-control/);
  await expect(page.getByRole('link', { name: /More Tools/ })).toBeVisible();
  await page.getByRole('link', { name: /More Tools/ }).click();
  await expect(page).toHaveURL(/\/review\/tools/);
  await page.getByRole('link', { name: /^Data Governance\b/ }).click();
  await expect(page).toHaveURL(/\/review\/data/);
  await expect(page.getByRole('heading', { name: 'Data Governance' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Backup / Export' })).toBeVisible();
});

test('LanguageOS imports dictionary assets and reviews lexical units recall-first', async ({ page }) => {
  const title = `Playwright Spanish-English ${Date.now()}`;
  const entries = [
    {
      headword: 'aprovechar',
      language: 'es',
      target_language: 'en',
      part_of_speech: 'verb',
      definition: 'to take advantage of; to make use of',
      translation: 'take advantage of, make use of',
      example_sentence: 'Debemos aprovechar esta oportunidad.',
      example_translation: 'We should take advantage of this opportunity.',
      collocations: ['aprovechar una oportunidad', 'aprovechar el tiempo'],
      usage_notes: ['Often used with opportunities, time, or resources.'],
    },
  ];

  await page.goto('/language/dictionaries');
  await expect(page.getByRole('heading', { name: 'Dictionary Kernel' })).toBeVisible();
  await expect(page.getByText('Draft lexical assets are not used in review until confirmed.')).toBeVisible();

  await page.getByLabel('Dictionary title').fill(title);
  await page.getByLabel('Dictionary type').selectOption('spanish_english');
  await page.getByLabel('Import format').selectOption('json');
  await page.getByLabel('Dictionary content').fill(JSON.stringify(entries, null, 2));
  const importDictionaryResponse = page.waitForResponse((response) =>
    response.url().includes('/api/language-os/dictionaries/import-json') &&
    response.request().method() === 'POST',
  );
  await page.getByRole('button', { name: /Import dictionary/ }).click();
  expect((await importDictionaryResponse).ok()).toBeTruthy();

  await expect(page.getByText(title).first()).toBeVisible();
  await expect(page.getByText('aprovechar').first()).toBeVisible();
  const assetArticle = page.locator('article').filter({ hasText: 'aprovechar' }).first();
  await expect(assetArticle.getByText('aprovechar una oportunidad')).toBeVisible();
  await expect(page.getByText(/#entry-1#sense-1/).first()).toBeVisible();
  await expect(page.getByText(/draft|needs_review/).first()).toBeVisible();

  const reviewBefore = await page.request.post(`${API_BASE}/api/language-os/review/generate-session`, {
    data: { max_units: 10 },
  });
  expect(reviewBefore.ok()).toBeTruthy();
  const beforePayload = await reviewBefore.json();
  expect(beforePayload.units.some((unit: any) => unit.headword === 'aprovechar')).toBeFalsy();

  await page.getByRole('button', { name: /Confirm dictionary/ }).click();
  await expect(page.getByText('confirmed').first()).toBeVisible();

  await assetArticle.getByRole('button', { name: /^Confirm$/ }).click();
  await expect(assetArticle.getByText('confirmed')).toBeVisible();

  await page.getByRole('link', { name: /Lexical review/ }).click();
  await expect(page).toHaveURL(/\/language\/review/);
  const generatedReviewResponse = page.waitForResponse((response) =>
    response.url().includes('/api/language-os/review/generate-session') &&
    response.request().method() === 'POST',
  );
  await page.getByRole('button', { name: /Generate lexical review/ }).click();
  const generatedReviewPayload = await (await generatedReviewResponse).json();
  expect(generatedReviewPayload.units.some((unit: any) => unit.headword === 'aprovechar')).toBeTruthy();

  for (let attempt = 0; attempt < generatedReviewPayload.units.length; attempt += 1) {
    if (await page.getByText(/aprovechar/).first().isVisible().catch(() => false)) break;
    await page.getByRole('button', { name: /Reveal answer/ }).click();
    const skipResponse = page.waitForResponse((response) =>
      response.url().includes('/api/language-os/review/units/') &&
      response.request().method() === 'POST',
    );
    await page.getByRole('button', { name: /Skip/ }).click();
    await skipResponse;
  }
  await expect(page.getByText(/aprovechar/).first()).toBeVisible();
  await expect(page.getByText('take advantage of')).toHaveCount(0);
  await page.getByPlaceholder('Write your answer before revealing.').fill('take advantage of the opportunity');
  await page.getByRole('button', { name: /Reveal answer/ }).click();

  await expect(page.getByText(/take advantage of/).first()).toBeVisible();
  await expect(page.getByText('We should take advantage of this opportunity.')).toBeVisible();
  await expect(page.getByText('aprovechar una oportunidad', { exact: true })).toBeVisible();
  await expect(page.getByText(/#entry-1#sense-1/).first()).toBeVisible();

  const partialResponse = page.waitForResponse((response) =>
    response.url().includes('/api/language-os/review/units/') &&
    response.request().method() === 'POST',
  );
  await page.getByRole('button', { name: /Partial/ }).click();
  await partialResponse;
  await expect(page.getByText(/Next review:/)).toBeVisible();
});

test('Formula Lab imports confirms and reviews formulas recall-first', async ({ page }) => {
  const targetFormula = 'WACC = w_d r_d (1 - t) + w_e r_e';
  const formulaNote = [
    `${targetFormula}.`,
    'w_d = debt weight; r_d = pre-tax cost of debt; t = tax rate; w_e = equity weight; r_e = cost of equity.',
    'Use when valuing the firm with a target capital structure.',
    'BA II Plus: enter cash flows, press NPV, enter WACC as I/Y, then CPT NPV.',
  ].join('\n');

  await page.goto('/review/formulas');
  await expect(page.getByRole('heading', { name: 'Formula Lab' })).toBeVisible();

  await page.getByLabel('Source title').fill('Playwright formula note');
  await page.getByLabel('Formula text').fill(formulaNote);
  await page.getByRole('button', { name: /Import formula/ }).click();

  await expect(page.getByText(targetFormula).first()).toBeVisible();
  await expect(page.getByText(/#seg-/).first()).toBeVisible();
  await page.getByLabel('Status').selectOption('draft');
  const waccArticle = page.locator('article').filter({ hasText: targetFormula }).filter({ hasText: 'BA II Plus: enter cash flows' }).first();
  await expect(waccArticle.getByText('draft')).toBeVisible();
  await waccArticle.getByRole('button', { name: /Confirm/ }).click();

  await page.getByRole('button', { name: /Start Formula Lab/ }).click();
  const panel = page.getByTestId('formula-session-panel');
  await expect(panel.getByText('Formula Review')).toBeVisible();
  let foundTargetFormula = false;
  for (let attempt = 0; attempt < 8; attempt += 1) {
    await expect(panel.getByText(targetFormula)).toHaveCount(0);
    const recallBox = panel.getByPlaceholder('Write the formula and variables before reveal.');
    if ((await recallBox.count()) === 0) break;
    await recallBox.fill('WACC = wd rd after tax + we re');
    await panel.getByRole('button', { name: /Reveal formula/ }).click();
    if (await panel.getByText(targetFormula).isVisible().catch(() => false)) {
      foundTargetFormula = true;
      break;
    }
    await panel.getByRole('button', { name: /skipped/ }).click();
  }

  expect(foundTargetFormula).toBeTruthy();
  await expect(panel.getByText('Variables')).toBeVisible();
  await expect(panel.getByText('BA II Plus', { exact: true })).toBeVisible();
  await expect(panel.getByText(/#seg-/).first()).toBeVisible();

  await panel.getByRole('button', { name: /partial/ }).click();
  await expect(panel.getByText(/Formula session complete|Formula Review/)).toBeVisible();
});

test('Coverage Audit seeds syllabus maps confirmed formula assets and links workflows', async ({ page }) => {
  await page.goto('/review/coverage');
  await expect(page.getByRole('heading', { name: 'Coverage Audit' })).toBeVisible();
  await expect(page.getByRole('button', { name: /missing/ })).toBeVisible();
  await expect(page.getByRole('button', { name: /partial/ })).toBeVisible();
  await expect(page.getByRole('button', { name: /covered/ })).toBeVisible();

  await page.getByRole('button', { name: /Seed demo syllabus/ }).click();
  await expect(page.locator('tr').filter({ hasText: 'Calculate and interpret WACC' }).first()).toBeVisible();
  await expect(page.getByText('Recommended Actions')).toBeVisible();

  const formulaNote = [
    'WACC = w_d r_d (1 - t) + w_e r_e.',
    'w_d = debt weight; r_d = pre-tax cost of debt; t = tax rate; w_e = equity weight; r_e = cost of equity.',
    'Use when valuing the firm with a target capital structure.',
    'BA II Plus: enter cash flows, press NPV, enter WACC as I/Y, then CPT NPV.',
  ].join('\n');
  const imported = await page.request.post(`${API_BASE}/api/review-lab/formulas/import-text`, {
    data: {
      profile_id: 'default',
      title: 'Playwright coverage WACC note',
      text: formulaNote,
    },
  });
  expect(imported.ok()).toBeTruthy();
  const importedPayload = await imported.json();
  const formula = importedPayload.assets.find((asset: any) => asset.asset_type === 'formula' || asset.formula_latex);
  expect(formula).toBeTruthy();
  const confirmed = await page.request.post(`${API_BASE}/api/review-lab/formulas/${formula.asset_id}/confirm`);
  expect(confirmed.ok()).toBeTruthy();

  await page.getByRole('button', { name: /Recompute coverage/ }).click();
  const waccRow = page.locator('tr').filter({ hasText: 'Calculate and interpret WACC' }).first();
  await expect(waccRow).toContainText(/partial|covered|weak|stale/);
  await expect(waccRow).toContainText(/C\s+[1-9]/);
  await expect(page.getByText(/create decision boundary asset|run Formula Lab|keep in scheduled review rotation/).first()).toBeVisible();

  await page.getByRole('link', { name: /Review Assets/ }).click();
  await expect(page).toHaveURL(/\/review\/assets/);
  await expect(page.getByRole('heading', { name: 'Review Assets' })).toBeVisible();

  await page.goto('/review/coverage');
  await page.getByRole('link', { name: /Formula Lab/ }).click();
  await expect(page).toHaveURL(/\/review\/formulas/);
  await expect(page.getByRole('heading', { name: 'Formula Lab' })).toBeVisible();
});

test('Mock Retro creates transfer gaps and generates correct-only Review Lab units', async ({ page }) => {
  const uniqueWrong = 'selected pretax debt cost in the WACC mock retro';
  const retroText = [
    'Q1 Corporate Issuers WACC',
    'LOS: CI-PLAY-RETRO',
    'Result: incorrect',
    'Confidence: high',
    'Time: 240s',
    `Wrong Output: ${uniqueWrong}`,
    'Correct Rule: WACC uses after-tax cost of debt: w_d * r_d * (1 - t) + w_e * r_e.',
    'Tested Formula: WACC',
    'BA II Plus: store weights and component costs, calculate weighted sum.',
    '',
    'Q2 Fixed Income Duration',
    'Result: incorrect',
    'Confidence: medium',
    'Boundary Rule: Use effective duration when cash flows can change.',
    'Correct Rule: Use effective duration for option-sensitive bonds.',
  ].join('\n');

  await page.goto('/review/mock-retro');
  await expect(page.getByRole('heading', { name: 'Mock Retro' })).toBeVisible();
  await page.getByLabel('Retro title').fill('Playwright Mock Retro');
  await page.getByLabel('Mock retro text').fill(retroText);
  await page.getByRole('button', { name: /Import retro/ }).click();

  await expect(page.getByText('Playwright Mock Retro')).toBeVisible();
  await page.getByRole('button', { name: /Analyze session/ }).click();

  await expect(page.getByText('confidence_mismatch').first()).toBeVisible();
  await expect(page.getByText(/formula_recall_gap|variable_confusion/).first()).toBeVisible();
  await expect(page.getByText('boundary_confusion').first()).toBeVisible();
  await expect(page.getByText(uniqueWrong)).toHaveCount(0);

  await page.getByRole('button', { name: /Generate Review Lab/ }).click();
  await expect(page).toHaveURL(/\/review\/lab\?session=/);
  await expect(page.getByRole('heading', { name: 'Review Lab' })).toBeVisible();
  await expect(page.getByText(/Recent mock transfer gap:/).first()).toBeVisible();
  await expect(page.getByText(uniqueWrong)).toHaveCount(0);

  await page.getByPlaceholder('Write your answer before revealing.').fill('after-tax cost of debt');
  await page.getByRole('button', { name: /Reveal Answer|Reveal Formula/ }).click();
  await expect(page.getByText(/after-tax cost of debt|effective duration/).first()).toBeVisible();
  await expect(page.getByText(uniqueWrong)).toHaveCount(0);
  await page.getByRole('button', { name: /Partial|partial/ }).click();
});

test('Tutor Copilot answers with grounded citations actions and hint mode', async ({ page }) => {
  const uniqueWrong = `UNIQUE_WRONG_TUTOR_E2E_${Date.now()}`;
  const formulaText = [
    'WACC = w_d r_d (1 - t) + w_e r_e.',
    'w_d = debt weight; r_d = pre-tax cost of debt; t = tax rate; w_e = equity weight; r_e = cost of equity.',
    'Use WACC when valuing a firm with target market value weights.',
    'BA II Plus: enter cash flows, press NPV, enter WACC as I/Y, then CPT NPV.',
  ].join('\n');

  const importedFormula = await page.request.post(`${API_BASE}/api/review-lab/formulas/import-text`, {
    data: {
      profile_id: 'default',
      title: 'Playwright Tutor WACC note',
      text: formulaText,
    },
  });
  expect(importedFormula.ok()).toBeTruthy();
  const formulaPayload = await importedFormula.json();
  const formula = formulaPayload.assets.find((asset: any) => asset.asset_type === 'formula' || asset.formula_latex);
  expect(formula).toBeTruthy();
  const confirmedFormula = await page.request.post(`${API_BASE}/api/review-lab/formulas/${formula.asset_id}/confirm`);
  expect(confirmedFormula.ok()).toBeTruthy();

  const importedDictionary = await page.request.post(`${API_BASE}/api/language-os/dictionaries/import-json`, {
    data: {
      title: 'Playwright Tutor Spanish Dictionary',
      dictionary_type: 'spanish_english',
      entries: [
        {
          headword: 'repasar',
          language: 'es',
          target_language: 'en',
          part_of_speech: 'verb',
          definition: 'to review or go over again',
          translation: 'review',
          example_sentence: 'Voy a repasar la formula WACC.',
          collocations: ['repasar una formula'],
        },
      ],
    },
  });
  expect(importedDictionary.ok()).toBeTruthy();
  const dictionaryPayload = await importedDictionary.json();
  await page.request.post(`${API_BASE}/api/language-os/dictionaries/${dictionaryPayload.dictionary.dictionary_id}/confirm`);
  await page.request.post(`${API_BASE}/api/language-os/lexical-assets/${dictionaryPayload.lexical_assets[0].lexical_id}/confirm`);

  const importedRetro = await page.request.post(`${API_BASE}/api/review-lab/mock-retro/import-text`, {
    data: {
      title: 'Playwright Tutor Retro',
      text: [
        'Q1 Corporate Issuers WACC',
        'Result: incorrect',
        `Wrong Output: ${uniqueWrong}`,
        'Correct Rule: WACC uses after-tax cost of debt.',
        'Tested Formula: WACC',
      ].join('\n'),
    },
  });
  expect(importedRetro.ok()).toBeTruthy();
  await page.request.post(`${API_BASE}/api/review-lab/mock-retro/sessions/${(await importedRetro.json()).session.mock_id}/analyze`);

  await page.goto('/review/tutor');
  await expect(page.getByRole('heading', { name: 'Tutor Copilot' })).toBeVisible();
  await page.getByRole('button', { name: /Formula Help/ }).click();
  await page.getByLabel('Tutor question').fill('Explain WACC and the calculator steps');
  await page.getByRole('button', { name: /^Ask$/ }).click();

  await expect(page.getByText(/Formula help:/).first()).toBeVisible();
  await expect(page.getByText(/BA II Plus steps/).first()).toBeVisible();
  await expect(page.getByText('Source Context')).toBeVisible();
  await expect(page.getByText(/#seg-/).first()).toBeVisible();
  await expect(page.getByText('Recommended Actions')).toBeVisible();
  await expect(page.getByRole('link', { name: /Practice in Formula Lab/ })).toBeVisible();
  await expect(page.getByText(uniqueWrong)).toHaveCount(0);

  await page.getByRole('button', { name: /^Hint$/ }).click();
  await page.getByLabel('Tutor question').fill('Give me a hint for WACC');
  await page.getByRole('button', { name: /^Ask$/ }).click();
  await expect(page.getByText(/Hint 1/).first()).toBeVisible();
  await expect(page.getByText(/Final answer/i)).toHaveCount(0);
  await expect(page.getByText(uniqueWrong)).toHaveCount(0);

  await page.getByRole('button', { name: /Language Help/ }).click();
  await page.getByLabel('Tutor question').fill('Explain repasar in context');
  await page.getByRole('button', { name: /^Ask$/ }).click();
  await expect(page.getByText(/repasar/).first()).toBeVisible();
  await expect(page.getByText(/review or go over again/).first()).toBeVisible();
  await expect(page.getByText(uniqueWrong)).toHaveCount(0);

  await page.getByRole('link', { name: /^Search$/ }).first().click();
  await expect(page).toHaveURL(/\/review\/search/);
  await page.goto('/review/tutor');
  await page.getByRole('link', { name: /Knowledge Map/ }).first().click();
  await expect(page).toHaveURL(/\/review\/knowledge-map/);
});

test('Goal onboarding creates an active goal readiness path and links core subsystems', async ({ page }) => {
  const goalTitle = `Playwright CFA Goal ${Date.now()}`;
  const wrongPhrase = `UNIQUE_WRONG_GOAL_ONBOARDING_E2E_${Date.now()}`;
  const attempt = await page.request.post(`${API_BASE}/api/attempts`, {
    data: {
      topic: 'Corporate Issuers',
      los: 'CI.Goal.Onboarding',
      prompt_or_question: 'Which debt cost belongs in WACC?',
      wrong_choice_or_output: wrongPhrase,
      correct_resolution: 'Use after-tax cost of debt in WACC.',
      error_type: 'concept_confusion',
      confidence: 1,
      time_spent: 60,
      evidence_refs: ['goal-onboarding-e2e'],
      is_correct: false,
    },
  });
  expect(attempt.ok()).toBeTruthy();

  await page.goto('/onboarding');
  await expect(page.getByRole('heading', { name: 'Onboarding' })).toBeVisible();
  await page.getByRole('button', { name: /^Exam$/ }).click();
  await page.getByRole('button', { name: /CFA-style Finance Study/ }).click();
  await page.getByLabel('Goal title').fill(goalTitle);
  await page.getByLabel('Weekly minutes').fill('480');
  await page.getByLabel('Energy mode').selectOption('normal');
  await page.getByRole('button', { name: /Create and activate goal/ }).click();

  await expect(page.getByText(goalTitle).first()).toBeVisible();
  await expect(
    page.getByText(/needs_import|ready_for_first_plan|needs_confirmation|ready_for_review|active/).first(),
  ).toBeVisible();
  await expect(page.getByText(wrongPhrase)).toHaveCount(0);

  await page.getByRole('button', { name: /Generate Day-1 plan/ }).click();
  await expect(page.getByText(/Import syllabus|Import the first local resource/).first()).toBeVisible();
  await expect(page.getByText('Open Mission Control')).toBeVisible();
  await expect(page.getByText('Create a safe local backup').first()).toBeVisible();
  await expect(page.getByText(wrongPhrase)).toHaveCount(0);

  await page.getByRole('link', { name: /^Planner$/ }).click();
  await expect(page).toHaveURL(/\/review\/study-planner/);
  await page.goto('/onboarding');
  await page.getByRole('link', { name: /^Mission$/ }).first().click();
  await expect(page).toHaveURL(/\/review\/mission-control/);
  await expect(page.getByText('Goal Readiness').first()).toBeVisible();
  await expect(page.getByText(goalTitle).first()).toBeVisible();
  await expect(page.getByText(wrongPhrase)).toHaveCount(0);

  await page.goto('/review/goals');
  await expect(page.getByRole('heading', { name: 'Goal Profiles' })).toBeVisible();
  await expect(page.getByText(goalTitle).first()).toBeVisible();
  await expect(page.getByRole('heading', { name: 'CFA-style Finance Study' })).toBeVisible();
  await expect(page.getByText(wrongPhrase)).toHaveCount(0);

  await page.setViewportSize({ width: 390, height: 820 });
  await page.goto('/onboarding');
  await expect(page.getByRole('heading', { name: 'Onboarding' })).toBeVisible();
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  expect(overflow).toBeLessThanOrEqual(4);
  await expect(page.getByText(wrongPhrase)).toHaveCount(0);
});

test('TASK-019 premium cockpit hides advanced tools behind More', async ({ page }) => {
  const wrongPhrase = `UNIQUE_WRONG_PREMIUM_COCKPIT_E2E_${Date.now()}`;
  const attempt = await page.request.post(`${API_BASE}/api/attempts`, {
    data: {
      topic: 'Corporate Issuers',
      los: 'CI.Premium.Cockpit',
      prompt_or_question: 'Which debt cost belongs in WACC?',
      wrong_choice_or_output: wrongPhrase,
      correct_resolution: 'Use after-tax cost of debt in WACC.',
      error_type: 'concept_confusion',
      confidence: 1,
      time_spent: 45,
      evidence_refs: ['premium-cockpit-e2e'],
      is_correct: false,
    },
  });
  expect(attempt.ok()).toBeTruthy();

  await page.goto('/review');
  await expect(page.getByRole('heading', { name: 'Today', exact: true })).toBeVisible();
  await expect(page.getByTestId('primary-cockpit')).toBeVisible();
  await expect(page.getByTestId('primary-cockpit').getByRole('link', { name: /start|continue|begin/i })).toBeVisible();
  await expect(page.getByRole('link', { name: /more|tools|advanced/i })).toBeVisible();
  await expect(page.getByTestId('primary-cockpit').getByText(/data governance/i)).toHaveCount(0);
  await expect(page.getByTestId('primary-cockpit').getByText(/interop/i)).toHaveCount(0);
  await expect(page.getByTestId('primary-cockpit').getByText(/route registry/i)).toHaveCount(0);
  await expect(page.getByText(wrongPhrase)).toHaveCount(0);

  await page.getByRole('link', { name: /more|tools|advanced/i }).click();
  await expect(page).toHaveURL(/\/review\/tools/);
  await expect(page.getByRole('heading', { name: /Tools|More/ })).toBeVisible();
  await expect(page.getByRole('link', { name: /Data Governance/ })).toBeVisible();
  await expect(page.getByRole('link', { name: /Interop/ })).toBeVisible();
  await expect(page.getByRole('link', { name: /Knowledge Map/ })).toBeVisible();
  await expect(page.getByRole('link', { name: /Search/ })).toBeVisible();
  await expect(page.getByText(wrongPhrase)).toHaveCount(0);

  await page.setViewportSize({ width: 390, height: 820 });
  await page.goto('/review');
  const cockpitOverflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  expect(cockpitOverflow).toBeLessThanOrEqual(4);
  await page.goto('/review/tools');
  const toolsOverflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  expect(toolsOverflow).toBeLessThanOrEqual(4);
});

test('TASK-019 Mission Control prioritizes actions and hides diagnostics', async ({ page }) => {
  await page.goto('/review/mission-control');

  await expect(page.getByRole('heading', { name: 'Mission Control' })).toBeVisible();
  await expect(page.getByText(/Top Recommendations|Next best steps/)).toBeVisible();
  await expect(page.getByText(/Advanced diagnostics/)).toBeVisible();
  await expect(page.getByText('Route Registry')).toHaveCount(0);
  await expect(page.getByText(/API checks|mounted/)).toHaveCount(0);

  await page.getByRole('button', { name: /Advanced diagnostics/ }).click();
  await expect(page.getByText('Route Registry')).toBeVisible();
});

test('Ecosystem Interop exports safe artifacts and imports drafts only', async ({ page }, testInfo) => {
  const uniqueWrong = `UNIQUE_WRONG_INTEROP_E2E_${Date.now()}`;
  const importId = `interop-import-${Date.now()}`;
  const formulaText = [
    'WACC = w_d r_d (1 - t) + w_e r_e.',
    'Use WACC when valuing a firm with a target market value capital structure.',
    'BA II Plus: enter cash flows, set I/Y to WACC, then CPT NPV.',
  ].join('\n');

  const importedFormula = await page.request.post(`${API_BASE}/api/review-lab/formulas/import-text`, {
    data: {
      profile_id: 'default',
      title: 'Playwright Interop WACC note',
      text: formulaText,
    },
  });
  expect(importedFormula.ok()).toBeTruthy();
  const formulaPayload = await importedFormula.json();
  const formula = formulaPayload.assets.find((asset: any) => asset.asset_type === 'formula' || asset.formula_latex);
  expect(formula).toBeTruthy();
  const confirmedFormula = await page.request.post(`${API_BASE}/api/review-lab/formulas/${formula.asset_id}/confirm`);
  expect(confirmedFormula.ok()).toBeTruthy();

  const wrongAttempt = await page.request.post(`${API_BASE}/api/attempts`, {
    data: {
      topic: 'Corporate Issuers',
      los: 'CI.Interop',
      prompt_or_question: 'Which debt cost belongs in WACC?',
      wrong_choice_or_output: uniqueWrong,
      correct_resolution: 'Use after-tax cost of debt in WACC.',
      error_type: 'concept_confusion',
      confidence: 1,
      time_spent: 45,
      evidence_refs: ['interop-e2e'],
      is_correct: false,
    },
  });
  expect(wrongAttempt.ok()).toBeTruthy();

  const todayPlan = await page.request.get(`${API_BASE}/api/study-planner/today?profile_id=default`);
  expect(todayPlan.ok()).toBeTruthy();

  const dataRoot = testInfo.config.metadata.openexamDataRoot as string | undefined;
  expect(dataRoot).toBeTruthy();
  const importDir = join(dataRoot as string, '.system', 'memory', 'interop', 'imports');
  mkdirSync(importDir, { recursive: true });
  const ankiImportFile = join(importDir, `${importId}.csv`);
  const ankiImportPath = `.system/memory/interop/imports/${importId}.csv`;
  writeFileSync(ankiImportFile, [
    'openexam_id,note_type,front,back,tags,source_refs,goal_id,topic_ids,quality_status,validation_status,created_at',
    `${importId},Concept,Interop import concept,Use confirmed source-backed rules.,interop,playwright#row=1,,,external,draft,2026-06-03T00:00:00Z`,
  ].join('\n'));
  const markdownImportFile = join(importDir, `${importId}.md`);
  const markdownImportPath = `.system/memory/interop/imports/${importId}.md`;
  writeFileSync(markdownImportFile, [
    '---',
    `openexam_id: markdown-${importId}`,
    'type: concept',
    'validation_status: draft',
    'source_refs:',
    '  - playwright-md#row=1',
    '---',
    '# Interop Markdown Import',
    '',
    'Correct rule/answer: Keep imported notes draft until manually confirmed.',
  ].join('\n'));

  await page.goto('/review/interop');
  await expect(page.getByRole('heading', { name: 'Ecosystem Interop' })).toBeVisible();
  const interopMain = page.locator('#main-content');
  await expect(interopMain.getByRole('link', { name: /Data Governance/ })).toBeVisible();
  await expect(interopMain.getByRole('link', { name: /Knowledge Map/ })).toBeVisible();
  await expect(interopMain.getByRole('link', { name: /^Goals$/ })).toBeVisible();
  await expect(interopMain.getByRole('link', { name: /Review Lab/ })).toBeVisible();
  await expect(interopMain.getByRole('link', { name: /^LanguageOS$/ })).toBeVisible();

  await page.getByLabel('Topic').fill('WACC');
  await page.getByRole('button', { name: /Export Anki/ }).click();
  await expect(page.getByText(/Anki artifact created:/)).toBeVisible();
  await expect(page.getByText(/Anki Csv|Anki Tsv/).first()).toBeVisible();
  await expect(page.getByText(uniqueWrong)).toHaveCount(0);

  await page.getByLabel('Import File Path').fill(ankiImportPath);
  await page.getByRole('button', { name: /Preview Anki Import/ }).click();
  await expect(page.getByText(/Anki preview:/)).toBeVisible();
  await expect(page.getByText('Auto Confirm').first()).toBeVisible();
  await page.getByRole('button', { name: /Commit Draft Import/ }).click();
  await expect(page.getByText(/Anki draft import committed:/)).toBeVisible();
  await expect(page.getByText(uniqueWrong)).toHaveCount(0);

  await page.getByRole('button', { name: /Markdown \/ Obsidian/ }).click();
  await page.getByRole('button', { name: /Export Markdown/ }).click();
  await expect(page.getByText(/Markdown artifact created:/)).toBeVisible();
  await expect(page.getByText(/Markdown Zip/).first()).toBeVisible();
  await page.getByLabel('Import File Path').fill(markdownImportPath);
  await page.getByRole('button', { name: /Preview Markdown Import/ }).click();
  await expect(page.getByText(/Markdown preview:/)).toBeVisible();
  await page.getByRole('button', { name: /Commit Markdown Drafts/ }).click();
  await expect(page.getByText(/Markdown draft import committed:/)).toBeVisible();
  await expect(page.getByText(uniqueWrong)).toHaveCount(0);

  await page.getByRole('button', { name: /^Calendar/ }).click();
  await page.getByRole('button', { name: /Export Calendar/ }).click();
  await expect(page.getByText(/Calendar artifact created:/)).toBeVisible();
  await expect(page.getByText(/Ics/).first()).toBeVisible();

  await page.getByRole('button', { name: /Learning Records/ }).click();
  await page.getByRole('button', { name: /Export Learning Records/ }).click();
  await expect(page.getByText(/Learning record artifact created:/)).toBeVisible();
  await expect(page.getByText(/Xapi Json/).first()).toBeVisible();
  await expect(page.getByText(uniqueWrong)).toHaveCount(0);

  await page.getByRole('link', { name: /Data Governance/ }).click();
  await expect(page).toHaveURL(/\/review\/data/);
  await page.goto('/review/interop');
  await page.getByRole('link', { name: /Knowledge Map/ }).click();
  await expect(page).toHaveURL(/\/review\/knowledge-map/);
});

test('TASK-020 Focus Session launches from cockpit and keeps one calm task visible', async ({ page }) => {
  const wrongPhrase = `UNIQUE_WRONG_FOCUS_E2E_${Date.now()}`;
  await seedFocusSessionSignals(page, wrongPhrase);
  const plan = await page.request.post(`${API_BASE}/api/study-planner/generate`, {
    data: { profile_id: 'default', energy_mode: 'high', available_minutes: 120, goal: 'WACC lexical focus' },
  });
  expect(plan.ok()).toBeTruthy();

  await page.goto('/review');
  await expect(page.getByTestId('primary-cockpit')).toBeVisible();
  await page.getByRole('link', { name: /Start Today|Start Focus Session|Continue Focus/ }).first().click();
  await expect(page).toHaveURL(/\/review\/focus/);

  await expect(page.getByRole('heading', { name: /Focus Session/ })).toBeVisible();
  const mainTask = page.getByTestId('focus-main-task');
  await expect(mainTask).toBeVisible();
  await expect(mainTask.getByText(/Step \d+ of \d+/)).toBeVisible();
  await expect(mainTask.getByText(/Target/i)).toBeVisible();
  await expect(page.getByText(/Data Governance|Ecosystem Interop|Route Registry/)).toHaveCount(0);
  await expect(page.locator('[data-testid="focus-step-grid"]')).toHaveCount(0);

  await expect(page.getByRole('button', { name: /Source evidence/ })).toBeVisible();
  await expect(page.getByText(/focus-e2e|dict-/)).toHaveCount(0);
  await page.getByRole('button', { name: /Source evidence/ }).click();
  await expect(mainTask.getByText(/focus-e2e|source|evidence/i).first()).toBeVisible();

  await expect(page.getByRole('button', { name: /Ask Tutor|Hint/ })).toBeVisible();
  await page.getByRole('button', { name: /Ask Tutor|Hint/ }).click();
  await expect(page.getByText(/Hint|evidence|unavailable/i).first()).toBeVisible();

  await page.keyboard.press('?');
  await expect(page.getByRole('heading', { name: 'Shortcuts' })).toBeVisible();
  await page.keyboard.press('Escape');
  await page.keyboard.press('r');
  await expect(page.getByText(wrongPhrase)).toHaveCount(0);
  await expect(page.getByText(/Correct answer|Correct rule|Formula|Meaning/).first()).toBeVisible();

  await page.keyboard.press('1');
  await expect(page.getByText(wrongPhrase)).toHaveCount(0);
  await expect(page.getByTestId('focus-progress')).toBeVisible();

  await page.setViewportSize({ width: 390, height: 820 });
  await page.goto('/review/focus');
  await expect(page.getByTestId('focus-main-task')).toBeVisible();
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  expect(overflow).toBeLessThanOrEqual(4);
});

test('TASK-020 Focus Session integrates planner mission control and final summary', async ({ page }) => {
  await seedFocusSessionSignals(page, `UNIQUE_WRONG_FOCUS_SUMMARY_${Date.now()}`);
  const generated = await page.request.post(`${API_BASE}/api/study-planner/generate`, {
    data: { profile_id: 'default', energy_mode: 'normal', available_minutes: 90, goal: 'Focus summary' },
  });
  expect(generated.ok()).toBeTruthy();

  await page.goto('/review/study-planner');
  await expect(page.getByRole('heading', { name: 'Study Planner' })).toBeVisible();
  await page.getByRole('link', { name: /Start as Focus Session|Start Focus Session/ }).first().click();
  await expect(page).toHaveURL(/\/review\/focus/);

  for (let index = 0; index < 20; index += 1) {
    if (await page.getByTestId('focus-summary').isVisible().catch(() => false)) break;
    const reveal = page.getByRole('button', { name: /Reveal|Show answer/ });
    if ((await reveal.isVisible().catch(() => false)) && (await reveal.isEnabled().catch(() => false))) {
      await reveal.click();
    }
    const complete = page.getByRole('button', { name: /Complete|Recalled/ }).first();
    if ((await complete.isVisible().catch(() => false)) && (await complete.isEnabled().catch(() => false))) {
      await clickFocusMutation(page, complete);
      continue;
    }
    const next = page.getByRole('button', { name: /Next/ }).first();
    if ((await next.isVisible().catch(() => false)) && (await next.isEnabled().catch(() => false))) {
      await clickFocusMutation(page, next);
      continue;
    }
    const skip = page.getByRole('button', { name: /Skip/ }).first();
    if ((await skip.isVisible().catch(() => false)) && (await skip.isEnabled().catch(() => false))) {
      await clickFocusMutation(page, skip);
    }
  }
  await expect(page.getByTestId('focus-summary')).toBeVisible();
  await expect(page.getByText(/Completed|Skipped|Blocked/).first()).toBeVisible();

  await page.goto('/review/mission-control');
  await expect(page.getByRole('heading', { name: 'Top Recommendations' })).toBeVisible({ timeout: 15_000 });
  const focusRecommendation = page.getByRole('link', { name: /Start Focus Session/ }).first();
  await expect(focusRecommendation).toBeVisible();
  await focusRecommendation.click();
  await expect(page).toHaveURL(/\/review\/focus/);
});

test('TASK-021 Focus reveal payload is hidden until explicit reveal', async ({ page }) => {
  await seedFocusSessionSignals(page, `UNIQUE_WRONG_FOCUS_REVEAL_UI_${Date.now()}`);
  const generated = await page.request.post(`${API_BASE}/api/study-planner/generate`, {
    data: { profile_id: 'default', energy_mode: 'high', available_minutes: 90, goal: 'Focus reveal contract' },
  });
  expect(generated.ok()).toBeTruthy();

  await page.goto('/review/focus?source=task-021-reveal');
  await expect(page.getByTestId('focus-main-task')).toBeVisible();
  const current = await page.request.get(`${API_BASE}/api/focus/current?profile_id=default`);
  expect(current.ok()).toBeTruthy();
  const session = (await current.json()).focus_session;
  const revealStep = session.steps.find((step: any) => step.embedded_payload?.reveal_payload?.correct_answer);
  expect(revealStep).toBeTruthy();
  const correctAnswer = revealStep.embedded_payload.reveal_payload.correct_answer;

  await expect(page.getByText(correctAnswer, { exact: false })).toHaveCount(0);
  await expect(page.getByRole('button', { name: /Source evidence/ })).toBeVisible();
  await expect(page.getByText(/Evidence/).first()).toHaveCount(0);
  await page.getByRole('button', { name: /Reveal/ }).click();
  await expect(page.getByText(correctAnswer, { exact: false }).first()).toBeVisible();
  await expect(page.getByText(/Data Governance|Ecosystem Interop|Route Registry/)).toHaveCount(0);
});

test('TASK-022 primary review and focus stay minimal while tools remain accessible', async ({ page }) => {
  await seedFocusSessionSignals(page, `UNIQUE_WRONG_TASK022_SURFACE_${Date.now()}`);
  const generated = await page.request.post(`${API_BASE}/api/study-planner/generate`, {
    data: { profile_id: 'default', energy_mode: 'normal', available_minutes: 90, goal: 'Task 022 surface guard' },
  });
  expect(generated.ok()).toBeTruthy();

  await page.goto('/review');
  await expect(page.getByTestId('primary-cockpit')).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Today', exact: true })).toBeVisible();
  await expect(page.getByText(/Data Governance|Ecosystem Interop|Route Registry/)).toHaveCount(0);
  await expect(page.getByRole('link', { name: /Start Focus Session/ }).first()).toBeVisible();

  await page.goto('/review/focus?source=task-022-surface');
  await expect(page.getByTestId('focus-main-task')).toBeVisible();
  await expect(page.getByTestId('focus-main-task')).toHaveCount(1);
  await expect(page.getByRole('button', { name: /Source evidence/ })).toBeVisible();
  await expect(page.getByText(/Evidence/).first()).toHaveCount(0);
  await expect(page.getByText(/Data Governance|Ecosystem Interop|Route Registry/)).toHaveCount(0);

  const skip = page.getByRole('button', { name: /Skip/ }).first();
  if ((await skip.isVisible().catch(() => false)) && (await skip.isEnabled().catch(() => false))) {
    await clickFocusMutation(page, skip);
  }

  await page.goto('/review/tools');
  await expect(page.getByRole('heading', { name: /Tools/ })).toBeVisible();
  await expect(page.getByRole('link', { name: /Data Governance/ })).toBeVisible();
  await expect(page.getByRole('link', { name: /Interop/ })).toBeVisible();
  await expect(page.getByRole('link', { name: /Knowledge Map/ })).toBeVisible();
  await expect(page.getByRole('link', { name: /Search/ })).toBeVisible();

  await page.setViewportSize({ width: 390, height: 820 });
  for (const route of ['/review', '/review/focus?source=task-022-mobile', '/review/tools']) {
    await page.goto(route);
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    expect(overflow).toBeLessThanOrEqual(4);
  }
});

async function clickFocusMutation(page: any, locator: any) {
  await Promise.all([
    page
      .waitForResponse((response: any) => response.url().includes('/api/focus/') && response.request().method() === 'POST')
      .catch(() => undefined),
    locator.click(),
  ]);
  await page.waitForTimeout(250);
}

async function clickReviewLabMutation(page: any, urlPattern: RegExp, locator: any) {
  await Promise.all([
    page
      .waitForResponse((response: any) => urlPattern.test(new URL(response.url()).pathname) && response.request().method() === 'POST')
      .catch(() => undefined),
    locator.click(),
  ]);
}

async function seedFocusSessionSignals(page: any, wrongPhrase: string) {
  const attempt = await page.request.post(`${API_BASE}/api/attempts`, {
    data: {
      topic: 'Corporate Issuers',
      los: 'CI.Focus',
      prompt_or_question: 'Which debt cost belongs in WACC?',
      wrong_choice_or_output: wrongPhrase,
      correct_resolution: 'Use after-tax cost of debt in WACC.',
      error_type: 'concept_confusion',
      confidence: 1,
      time_spent: 45,
      evidence_refs: ['focus-e2e'],
      is_correct: false,
    },
  });
  expect(attempt.ok()).toBeTruthy();
  const dailyReview = await page.request.get(`${API_BASE}/api/daily-review/today`);
  expect(dailyReview.ok()).toBeTruthy();

  const formula = await page.request.post(`${API_BASE}/api/review-lab/formulas/import-text`, {
    data: {
      profile_id: 'default',
      title: 'Focus WACC note',
      text: [
        'WACC = w_d r_d (1 - t) + w_e r_e.',
        'Use WACC when valuing a firm with a target market value capital structure.',
        'BA II Plus: enter cash flows, set I/Y to WACC, then CPT NPV.',
      ].join('\n'),
    },
  });
  expect(formula.ok()).toBeTruthy();
  const formulaAsset = (await formula.json()).assets.find((asset: any) => asset.asset_type === 'formula' || asset.formula_latex);
  expect(formulaAsset).toBeTruthy();
  expect((await page.request.post(`${API_BASE}/api/review-lab/formulas/${formulaAsset.asset_id}/confirm`)).ok()).toBeTruthy();

  const dictionary = await page.request.post(`${API_BASE}/api/language-os/dictionaries/import-json`, {
    data: {
      title: 'Focus Spanish Dictionary',
      dictionary_type: 'spanish_english',
      entries: [
        {
          headword: 'aprovechar',
          language: 'es',
          target_language: 'en',
          part_of_speech: 'verb',
          definition: 'to take advantage of; to make use of',
          translation: 'take advantage of',
          example_sentence: 'Debemos aprovechar esta oportunidad.',
          collocations: ['aprovechar una oportunidad'],
        },
      ],
    },
  });
  expect(dictionary.ok()).toBeTruthy();
  const dictionaryPayload = await dictionary.json();
  expect((await page.request.post(`${API_BASE}/api/language-os/dictionaries/${dictionaryPayload.dictionary.dictionary_id}/confirm`)).ok()).toBeTruthy();
  expect((await page.request.post(`${API_BASE}/api/language-os/lexical-assets/${dictionaryPayload.lexical_assets[0].lexical_id}/confirm`)).ok()).toBeTruthy();
}
