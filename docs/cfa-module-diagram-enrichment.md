# CFA Module Diagram Enrichment

## Purpose

`CFA_tier1/` diagrams are review accelerators, not decorative assets.
They should turn dense module text, tables, and repeated mistake patterns into visual decision paths that change the next study action.

## Default Format

- Prefer Mermaid blocks inside Markdown for maintainability.
- Keep diagrams close to the relevant module, usually in `## 核心图解`.
- Mermaid sizing is controlled by `.obsidian/snippets/cfa-mermaid-responsive.css`; keep this snippet enabled so diagrams fit the Obsidian note container.
- Use raster image generation only when Mermaid cannot express the required visual, such as realistic chart shapes, curves, or annotated conceptual figures.
- Do not place project-referenced generated images outside the repository.

## Scope Rules

- Formal module and MOC files may receive `核心图解`.
- `_legacy/`, `_archive/`, dashboard, and mock projection files should not be manually diagram-enriched.
- Obsidian remains the projection layer; source learning evidence still comes from `.system/events/` and `.system/memory/`.

## Quality Bar

Each diagram should answer at least one of these:

- Which formula or framework should I select?
- Which branch does the question trigger?
- Which table comparison is easier to remember as a flow?
- Which mistake pattern does this prevent?

Avoid diagrams that only restate headings without adding decision value.
