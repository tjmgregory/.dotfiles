---
name: cascading-specs
description: >
  Auto-discovers project specifications and guides next steps via cascade principle.
  On invoke: scans for existing docs (vision, requirements, use cases, entity model,
  architecture, tests), identifies gaps, recommends what to create next. Changes flow
  downward only—updating a requirement cascades to use cases, tests, code.
  Use when starting work, adding features, reviewing spec coverage, or updating docs.
  Triggers: "what specs exist", "spec status", "cascade", "next doc", "what should I write",
  "review specs", "UP", "unified process".
---

# Cascading Specs

Specifications-driven development where specs drive code, not reverse. Changes cascade downward through the hierarchy.

## On Invoke: Discovery First

Before doing anything else, discover the current state:

### Step 1: Find Existing Specs

```bash
# Look for spec directories
ls -la docs/ specifications/ specs/ design/ 2>/dev/null

# Look for identifier patterns in markdown files
grep -r "G-[0-9]\|REQ-[0-9]\|NFR-[0-9]\|UC-[0-9]\|TC-[0-9]\|ADR-[0-9]" --include="*.md" . 2>/dev/null | head -30
```

Also glob for common spec filenames:
- `**/vision*.md`, `**/goals*.md`
- `**/requirements*.md`, `**/reqs*.md`
- `**/use-case*.md`, `**/usecases*.md`
- `**/entity*.md`, `**/domain*.md`
- `**/architecture*.md`, `**/design*.md`
- `**/acceptance*.md`, `**/tests*.md`

### Step 2: Assess State

Report findings to user:
- Which artifacts exist (with paths)
- Which are missing from the cascade
- Current cascade coverage (e.g., "Vision → Requirements → [gap] → Tests")

### Step 3: Recommend Next Step

Based on cascade hierarchy, suggest what to create next:

```
Vision (WHY)
    ↓
Requirements (WHAT must it do)
    ↓
Use Cases (HOW actors achieve goals)
    ↓
Entity Model + Architecture (WHAT concepts, HOW structured)
    ↓
Acceptance Tests (HOW to verify)
    ↓
Code
```

**Cascade rule**: Always fill gaps top-down. No use cases without requirements. No tests without something to trace to.

## The Cascade Principle

Changes flow **downward only**:

| If this changes... | Update these downstream |
|-------------------|------------------------|
| Vision/Goals | Requirements, Use Cases, Tests, Code |
| Requirements | Use Cases, Tests, Code |
| Use Cases | Tests, Code |
| Entity Model | Architecture, Code |
| Architecture | Code |
| Tests | Code only |

**When a spec changes**:
1. Identify the identifier (e.g., REQ-003)
2. Grep codebase for that identifier
3. Update all downstream artifacts that reference it

## Writing Specs

When creating or updating an artifact, load the appropriate reference:

| Artifact | Reference |
|----------|-----------|
| Vision | [references/vision.md](references/vision.md) |
| Requirements | [references/requirements-catalogue.md](references/requirements-catalogue.md) |
| Use Cases | [references/use-cases.md](references/use-cases.md) |
| Entity Model | [references/entity-model.md](references/entity-model.md) |
| Architecture | [references/software-architecture.md](references/software-architecture.md) |
| Acceptance Tests | [references/acceptance-tests.md](references/acceptance-tests.md) |
| NFRs/Supplementary | [references/supplementary-specifications.md](references/supplementary-specifications.md) |

Templates available in `assets/templates/` for new artifacts.

## Identifier Conventions

| Prefix | Document |
|--------|----------|
| G- | Vision / Goals |
| REQ- | Functional Requirements |
| NFR- | Non-Functional Requirements |
| UC- | Use Cases |
| TC- | Test Cases |
| ADR- | Architecture Decision Records |

Consistency matters more than convention—match existing project patterns.

## Quick Decisions

**Starting fresh?** Create `docs/specs/` with vision.md first.

**Adding a feature?** Check if requirements exist → add REQ-xxx → add UC-xxx → add TC-xxx.

**Found a bug?** Trace: is this a missing requirement, incomplete use case, or just wrong code?

**Which artifacts for your project?** See [references/artefact-index.md](references/artefact-index.md) for project-type recommendations.

## Common Mistakes

- **Requirements prescribing solutions**: "Use PostgreSQL" → move to architecture
- **Use cases with UI details**: "Click blue button" → wrong. "Initiates checkout" → correct
- **Entity model as DB schema**: PKs, FKs, SQL types → wrong. Business concepts → correct
- **Skipping cascade levels**: Tests without requirements → add the requirements first
