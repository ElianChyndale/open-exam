import type { Meta, StoryObj } from '@storybook/nextjs-vite';
import { http, HttpResponse } from 'msw';
import Capture from './capture/page';
import Dashboard from './dashboard/page';
import Diagnosis from './diagnosis/page';
import Institution from './institution/page';
import Mock from './mock/page';
import Review from './review/page';
import Today from './today/page';

const handlers = [
  http.get('http://localhost:8000/api/study-plan/today', () => HttpResponse.json({
    plan_id: 'sp-story',
    date: '2026-05-31',
    energy_level: 3,
    available_minutes: 120,
    focus_topic: 'Fixed Income',
    focus_reason: 'Two due retrieval drills',
    high_energy_tasks: [{ task_type: 'difficult_practice', description: 'Duration and convexity comparison', fit: 0.92 }],
    moderate_energy_tasks: [{ task_type: 'mistake_review', description: 'Revisit curve interpretation', fit: 0.78 }],
    low_energy_tasks: [{ task_type: 'formula_drill', description: 'Recall effective duration formula', fit: 0.7 }],
    danger_los_list: ['FI / Duration', 'Economics / FX quotes'],
    warnings: ['One high-confidence error is due for review.'],
  })),
  http.get('http://localhost:8000/api/diagnose/patterns', () => HttpResponse.json({ patterns: [] })),
  http.get('http://localhost:8000/api/attempts/recent', () => HttpResponse.json({ attempts: [] })),
  http.get('http://localhost:8000/api/review-pack/today', () => HttpResponse.json({
    markdown_content: '# Today\\n\\n## Retrieval\\n\\n- Recall duration before revealing the answer.',
  })),
  http.get('http://localhost:8000/api/mock/history', () => HttpResponse.json({ sessions: [] })),
  http.get('http://localhost:8000/api/dashboard/effectiveness', () => HttpResponse.json({
    report_id: 'report-story',
    period_start: '2026-05-01',
    period_end: '2026-05-31',
    due_review_completion_rate: 0.78,
    high_confidence_error_count: 2,
    interleaving_accuracy: 0.64,
    same_error_recurrence_rate: 0.12,
    los_risk_heatmap: { 'Fixed Income/Duration': 0.8, 'Economics/FX': 0.45 },
    danger_top_3: ['Fixed Income/Duration'],
    predicted_pass_probability: 0.73,
    confidence_band_low: 0.66,
    confidence_band_high: 0.79,
    calibration_trend: 'improving',
    error_count_trend: [4, 3, 2],
  })),
  http.get('http://localhost:8000/api/dashboard/summary', () => HttpResponse.json({
    total_questions_recorded: 42,
    due_review_items: 6,
    active_patterns: 2,
  })),
  http.get('http://localhost:8000/api/institution/cohorts', () => HttpResponse.json({ cohorts: [] })),
];

const meta = {
  title: 'Routes/Existing Workspace',
  component: Today,
  parameters: {
    layout: 'fullscreen',
    msw: { handlers },
  },
  decorators: [
    (Story: () => JSX.Element) => <main className="min-h-screen bg-surface-canvas p-6"><Story /></main>,
  ],
} satisfies Meta<typeof Today>;

export default meta;
type Story = StoryObj<typeof meta>;

export const TodayRoute: Story = {};
export const CaptureRoute: Story = { render: () => <Capture /> };
export const DiagnosisRoute: Story = { render: () => <Diagnosis /> };
export const ReviewRoute: Story = { render: () => <Review /> };
export const MockRoute: Story = { render: () => <Mock /> };
export const DashboardRoute: Story = { render: () => <Dashboard /> };
export const InstitutionRoute: Story = { render: () => <Institution /> };
