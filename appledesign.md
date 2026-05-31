# OpenExam Apple-Style Design Contract

OpenExam is a light-first macOS productivity workspace for deliberate study. It should feel calm, precise, and information-dense without looking heavy.

## Principles

- Use semantic design tokens only. Route components must not embed color literals.
- Default to a warm, quiet light canvas with translucent raised surfaces. Support adaptive dark mode with the same hierarchy.
- Keep translucency restrained: use it for the navigation rail, cards, and sheets where depth clarifies structure.
- Prefer compact controls, generous page margins, rounded rectangles, subtle separators, and tabular metrics.
- Preserve visible `:focus-visible` rings for keyboard users.
- Respect `prefers-reduced-motion`; motion should never be required to understand state.
- Treat mobile as a first-class workspace. Navigation becomes a bottom bar and pages retain readable spacing.

## Semantic Tokens

| Token | Purpose |
|---|---|
| `surface-canvas` | Application background |
| `surface-raised` | Cards, sheets, navigation |
| `surface-field` | Inputs, inset rows, code panels |
| `surface-hover` | Hovered rows and controls |
| `line` | Quiet separators |
| `ink` | Primary text |
| `muted` | Secondary text |
| `accent` | Selected states and primary actions |
| `success`, `warning`, `danger` | Status communication |

## Component Rules

- Buttons use `button-primary` or semantic surface classes. Disabled state remains legible.
- Inputs use `field`; focus is visible in both themes.
- Cards use `card`; do not add bespoke background colors per route.
- Alerts pair semantic border and surface tokens with text labels. Color is supporting evidence, not the only signal.
- Loading and empty states remain compact and actionable.
- Daily Review answers stay concealed until the learner chooses to reveal them.
