# CFA_tier1 Vault Restructure Design

> Note: This design document reflects the first restructuring pass. The current live vault has since been refined into subject-based directories such as `Quantitative_Methods/`, `Ethical_and_Professional_Standards/`, and `dashboard/`.

## Goal

Restructure the repository so it behaves like an Obsidian-first CFA Level I vault while preserving the local agent system. The old `obsidian/` export directory will be replaced by a full content-facing `CFA_tier1/` tree, a root `.obsidian/` config directory will be added, and the Python workflows will export projection pages into the new vault layout.

## Why This Change

The current repository is technically correct for the agent system, but it is not pleasant to browse inside Obsidian because:

- the reading layer is just a thin `obsidian/` export folder
- study notes live at the repository root instead of inside a vault hierarchy
- there is no `.obsidian/` directory to represent vault configuration
- exported pages are not grouped separately from curated study content

The target is to imitate the screenshot pattern: one visible study vault directory, one hidden `.obsidian/` configuration directory, and a cleaner top-level structure that keeps content easier to scan.

## Target Structure

```text
CFA_learning/
├── .obsidian/
├── CFA_tier1/
│   ├── 00-Index.md
│   ├── 00-Overview/
│   ├── 01-Quantitative/
│   ├── 02-Ethics/
│   ├── 03-FRA/
│   ├── 04-Corporate-Issuers/
│   ├── 05-Equity/
│   ├── 06-Fixed-Income/
│   ├── 07-Derivatives/
│   ├── 08-Alternative-Investments/
│   ├── 09-Portfolio-Management/
│   └── 90-Exports/
├── .system/
│   ├── app/
│   ├── events/
│   ├── memory/
│   ├── evals/
│   └── tests/
├── log/
├── schedule/
├── scripts/
├── skills/
├── AGENTS.md
├── README.md
└── pyproject.toml
```

## Scope

### Content-facing layer

- replace `obsidian/` with `CFA_tier1/`
- move the existing study markdown files into `CFA_tier1/`
- add an index note so the vault has a clear entry point
- reserve `CFA_tier1/90-Exports/` for generated projection pages

### System-facing layer

- move `app/`, `events/`, `memory/`, `evals/`, and `tests/` under `.system/`
- keep `skills/` top-level because it is both system structure and a user-visible workflow contract
- keep `AGENTS.md`, `README.md`, and `pyproject.toml` at the repository root

### Workflow changes

- `Repository` must resolve all core paths from the new `.system/` layout
- Obsidian export pages must be written to `CFA_tier1/90-Exports/`
- tests must assert against the new paths
- docs must describe `CFA_tier1/` as the Projection Layer and `.obsidian/` as configuration only

## `.obsidian` Meaning

`.obsidian/` is not primary knowledge storage. It is the vault configuration directory used by the Obsidian application for workspace state, plugin settings, appearance, and related metadata. The source of truth remains `.system/events/` and `.system/memory/`, while `CFA_tier1/` is the projection and reading surface.

## Boundaries and Non-Goals

- do not collapse raw evidence into `CFA_tier1/`
- do not move `skills/` under `.system/` in this change
- do not redesign CLI commands or data models unless path changes require it
- do not invent Obsidian content beyond basic vault scaffolding and the existing notes

## Expected Behavioral Result

- opening the repository in Obsidian shows a vault-like structure centered on `CFA_tier1/`
- generated pages land in `CFA_tier1/90-Exports/`
- the Python CLI continues to work with the new filesystem layout
- tests prove that exports overwrite the same files instead of duplicating them
