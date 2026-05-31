import type { Meta, StoryObj } from '@storybook/nextjs-vite';
import { http, HttpResponse } from 'msw';
import Capture from './capture/page';
import Dashboard from './dashboard/page';
import Diagnosis from './diagnosis/page';
import Institution from './institution/page';
import MapPage from './map/page';
import Mock from './mock/page';
import Practice from './practice/page';
import Review from './review/page';
import Settings from './settings/page';
import Setup from './setup/page';
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
  http.get('http://localhost:8000/api/profile', () => HttpResponse.json({
    profile: {
      exam_date: '2026-11-15',
      current_phase: 'review',
      target_score_percentile: 75,
      daily_minutes_available: 120,
      weekly_study_days: 6,
      preferred_session_minutes: 50,
      peak_energy_window: '08:00-11:00',
      moderate_energy_window: '14:00-18:00',
      low_energy_window: '20:00-22:00',
    },
  })),
  http.get('http://localhost:8000/api/curriculum', () => HttpResponse.json({
    subject_count: 10,
    module_count: 93,
    subjects: [{
      subject: 'Fixed Income',
      exam_weight: '11-14%',
      module_count: 19,
      modules: [{ module: 'M01', official_module: 'Module 1: Fixed-Income Instrument Features', los: ['describe bond features'] }],
    }],
  })),
  http.get('http://localhost:8000/api/tasks/today', () => HttpResponse.json({
    tasks: [{ task_id: 'task-story', title: 'Complete due retrieval review', status: 'pending', task_type: 'active_recall', estimated_minutes: 25, priority: 95, energy_fit: 'moderate', topic: 'Fixed Income' }],
  })),
  http.get('http://localhost:8000/api/notifications', () => HttpResponse.json({ notifications: [] })),
  http.post('http://localhost:8000/api/review-sessions', () => HttpResponse.json({
    session_id: 'review-story',
    items: [{ prompt_id: 'prompt-story', prompt_text: 'Recall the duration rule.', answer_text: 'Use effective duration when cash flows can change.', topic: 'Fixed Income', los: 'FI.Duration' }],
  })),
  http.get('http://localhost:8000/api/question-banks/quarantine', () => HttpResponse.json({ questions: [] })),
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
export const SetupRoute: Story = { render: () => <Setup /> };
export const SettingsRoute: Story = { render: () => <Settings /> };
export const MapRoute: Story = { render: () => <MapPage /> };
export const PracticeRoute: Story = { render: () => <Practice /> };
