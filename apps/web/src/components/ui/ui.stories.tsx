import type { Meta, StoryObj } from '@storybook/nextjs-vite';
import { Alert, Badge, Button, EmptyState, Field, ListRow, Metric, SearchField, Select, Sheet, Surface, TextArea } from './ui';

const meta = {
  title: 'Foundation/Apple Workspace Kit',
  component: Surface,
  parameters: { layout: 'centered' },
} satisfies Meta<typeof Surface>;

export default meta;
type Story = StoryObj<typeof meta>;

export const PrimitiveGallery: Story = {
  render: () => (
    <Surface className="w-[min(760px,90vw)] space-y-5">
      <div>
        <p className="metric-label">OpenExam UI Foundation</p>
        <h1 className="mt-1 text-2xl font-semibold tracking-tight">Apple workspace primitives</h1>
      </div>
      <div className="flex flex-wrap gap-2">
        <Button>Start review</Button>
        <Button variant="secondary">Open map</Button>
        <Button variant="ghost">Dismiss</Button>
        <Button variant="danger">Skip task</Button>
      </div>
      <div className="flex flex-wrap gap-2">
        <Badge tone="accent">Official registry</Badge>
        <Badge tone="success">Completed</Badge>
        <Badge tone="warning">Due today</Badge>
        <Badge tone="danger">High risk</Badge>
      </div>
      <div className="grid gap-3 md:grid-cols-3">
        <Metric label="Due reviews" value="12" detail="4 high-confidence errors" />
        <Metric label="Study window" value="90 min" detail="Peak energy" />
        <Metric label="Weak LOS" value="3" detail="Needs retrieval" />
      </div>
      <Alert>Run a short retrieval drill before opening the answer.</Alert>
      <div className="grid gap-3 md:grid-cols-2">
        <Field aria-label="Exam date" type="date" />
        <Select aria-label="Study phase" defaultValue="review"><option value="review">Review phase</option></Select>
        <TextArea aria-label="Reflection" placeholder="What changed your decision?" />
        <SearchField aria-label="Search knowledge" placeholder="Search modules, formulas, traps..." />
      </div>
      <ListRow>LOS review rows stay quiet until they need attention.</ListRow>
      <Sheet title="Empty state"><EmptyState title="Nothing due yet" detail="New cards appear after a mistake is captured." /></Sheet>
    </Surface>
  ),
};
