# OpenExam Apple Workspace Design Contract

## Product Character

OpenExam is a calm CFA Level I learning workspace, not a dense admin cockpit. It should feel like a native macOS study tool: precise, quiet, and trustworthy under repeated daily use.

## Visual Rules

- Use a light-first system-adaptive palette with semantic tokens only. Dark mode follows `prefers-color-scheme`.
- Use layered white or charcoal surfaces, restrained translucency, subtle borders, and soft window-like shadows.
- Reserve blue for primary actions, green for confirmed progress, amber for attention, and red for evidence-backed risk.
- Keep density comfortable: 16px surface radii, 10-12px controls, short labels, and generous breathing room.
- Prefer the platform font stack to preserve the macOS workspace character.
- Do not embed color literals in route components. Use shared Tailwind semantic colors or UI primitives.

## Interaction Rules

- Every interactive element must expose a visible keyboard focus state.
- Honor `prefers-reduced-motion`; motion should orient rather than decorate.
- Desktop uses a translucent left sidebar. Mobile uses bottom tabs: `Today`, `Practice`, `Coach`, `More`.
- Mobile feature access must match desktop feature access through the `More` sheet.
- Empty, loading, success, warning, and error states are first-class interface states.

## Component Rules

- Build new screens from the primitives in `apps/web/src/components/ui/ui.tsx`.
- Use `Surface` or `Sheet` for grouped information, `Button` for actions, `Field` / `TextArea` / `Select` for controls, and `Alert` for actionable warnings.
- Metrics use tabular numerals and concise labels.
- Generated evidence and personal edits must be visually distinguishable in knowledge views.
