---
name: unified-process
description: >
  Guide for following the Unified Process methodology with AI agents. Use when:
  (1) Creating or reviewing UP artefacts (vision, requirements, use cases, entity model, architecture, acceptance tests, supplementary specs),
  (2) Setting up UP document structure in a new project,
  (3) Applying the cascade principle when documents change,
  (4) Validating document boundaries (requirements vs use cases vs architecture).
  Trigger on: "UP", "unified process", "AIUP", "write vision", "write requirements", "review use case", "cascade change", "document hierarchy".
---

# Unified Process

Specifications-driven development where specs drive code, not the reverse.

## Core Principles

1. **Traceability via identifiers**: G-001 (goals) → REQ-001 (requirements) → UC-001 (use cases) → TC-001 (tests)
2. **Cascade principle**: Changes flow downward only. Changing a goal may affect everything; changing a test affects only code.
3. **Appropriate abstraction**: Each document type has a specific level. Don't mix concerns.
4. **Requirements describe needs, not solutions**: "Data must persist durably" (need) vs "Use PostgreSQL" (solution)
5. **Specs drive code, not reverse** (AIUP): When reality diverges from specs, update specs first. Code is regenerable.
6. **Iterative refinement**: Specifications, code, and tests improve together through short cycles. Perfect specs are impossible—iterate.

## Document Hierarchy

```
Vision (G-001, G-002...)           ← WHY are we building this?
    ↓
Requirements (REQ-001, NFR-001...)  ← WHAT must the system do?
    ↓
Use Cases (UC-001, UC-002...)       ← HOW do actors achieve goals?
    ↓
Entity Model + Architecture         ← WHAT concepts exist? HOW is it structured?
    ↓
Acceptance Tests (TC-001...)        ← HOW do we verify it works?
    ↓
Code
```

## Workflows

### Creating a new artefact

1. Identify the artefact type needed
2. Read the catalogue definition: `references/<artefact>.md`
3. Use the template from `assets/templates/` if available
4. Write the document following "Should contain" guidance
5. Validate against the checklist in the catalogue
6. Verify traceability (IDs link upstream)

### Reviewing an artefact

1. Read the catalogue definition for that artefact type
2. Check against "Should NOT contain" list — common mistakes
3. Verify examples match "Good" patterns, not "Bad"
4. Confirm appropriate abstraction level
5. Validate traceability chain

### When a document changes (cascade)

1. Identify what changed and its identifier (e.g., REQ-001)
2. Search codebase for that identifier
3. Create tickets for each affected downstream artefact:
   - Requirements change → update use cases, tests, code
   - Use case change → update tests, code
   - Test change → update code only
4. Changes do NOT ripple upward

### Setting up UP in a new project

1. Create `docs/unified-process/` directory
2. Copy templates from `assets/templates/` as starting points
3. Decide which artefacts to use (see "Minimum Viable Process" below)
4. Link UP work to issue tracker using identifiers

## Minimum Viable Process

For simple projects, you may only need:
- **Vision** (one paragraph + goals)
- **Requirements** (bullet list with IDs)
- **Acceptance Tests** (how you know it works)

Add more artefacts as complexity grows. See `references/artefact-index.md` for the complete catalogue of all possible UP artefacts and when to use each.

## When to Suggest Additional Artefacts

**Suggest a Business Case** when: Justifying budget, competing for resources, need ROI tracking.

**Suggest a Stakeholder Map** when: Multiple groups with conflicting interests, political complexity.

**Suggest a Risk Register** when: Significant unknowns, high-stakes project, need to communicate risks.

**Suggest a Glossary** when: Team uses terms inconsistently, domain is unfamiliar.

**Suggest ADRs** when: Team turnover, long-lived system, need to explain "why we did it this way."

**Suggest API Specification** when: Building APIs for consumers, contract-first development.

**Suggest Deployment Runbook** when: Complex deployment, ops team different from dev team.

For the full decision guide, consult `references/artefact-index.md`.

## Artefact Quick Reference

| Artefact | Purpose | Key Rule |
|----------|---------|----------|
| Vision | Why + what success looks like | Goals are measurable outcomes, not features |
| Requirements | What the system must do | Needs, not solutions. No tech names. |
| Use Cases | How actors achieve goals | Goal-oriented, not function-oriented. No UI details. |
| Entity Model | Core business concepts | NOT a database schema. No PKs, no SQL types. |
| Architecture | System structure + decisions | Components + rationale. No code. |
| Acceptance Tests | Verify requirements met | Business language. Observable behaviour only. |
| Supplementary Specs | NFRs + cross-cutting concerns | Measurable. FURPS+ categories. |

For detailed guidance on any artefact, read `references/<artefact>.md`.

## Common Boundary Violations

**Requirements becoming use cases**: If you're writing interaction steps, it's a use case.

**Use cases becoming UI specs**: "User clicks blue button" → wrong. "User initiates checkout" → correct.

**Entity model becoming database schema**: Primary keys, foreign keys, SQL types → wrong. Business concepts → correct.

**Architecture including code**: Function definitions → wrong. Component responsibilities → correct.

**Requirements prescribing solutions**: Technology names in requirements → move to architecture.

## Identifier Conventions

| Prefix | Document |
|--------|----------|
| G- | Vision / Goals |
| REQ- | Functional Requirements |
| NFR- | Non-Functional Requirements |
| UC- | Use Cases |
| TC- | Test Cases |
| ADR- | Architecture Decision Records |

Consistency matters more than convention—use what fits your project.
