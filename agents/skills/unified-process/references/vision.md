# Vision Document

## Purpose

The Vision establishes **why we're building this system** and **what success looks like**. It captures shared understanding about the problem being solved and the high-level shape of the solution.

The Vision is the **most stable** document. If it changes frequently, you don't have a clear vision—you have ongoing discovery.

## Should Contain

### Problem Statement
- Concrete (not "things are inefficient" but "manual data entry takes 40 hours per week")
- Stakeholder-focused (whose problem?)
- Measurable (how do we know the problem exists?)

### Solution Overview
High-level description of what the system does. NOT a feature list—the conceptual approach.

### Goals (G-001, G-002, ...)
- Unique identifiers for traceability
- Measurable (you can tell if achieved)
- Outcome-focused (what changes in the world)
- Stable (don't change frequently)

### Non-Goals
Explicitly what the system will NOT do. Prevents scope creep.

### Target Users
Who will use this? Primary vs secondary users.

### Success Metrics
Business outcomes, not technical metrics.
- Good: "Revenue from automated sales increases 20%"
- Bad: "System has 99.9% uptime" (that's an NFR)

### Key Constraints
Timeline, budget, technical, regulatory, organisational.

## Should NOT Contain

- **Feature lists**: "Dashboard with sidebar" → wrong level
- **Technical decisions**: "Use microservices" → architecture
- **Detailed requirements**: "Filter by date range" → requirements catalogue
- **Use cases**: Interaction flows belong elsewhere
- **Implementation timeline**: Separate artefact

## Good vs Bad Examples

### Goals

**Good:**
> G-001: Reduce manual data entry time by 80%

Measurable, outcome-focused, stable.

**Bad:**
> G-001: Build an automated data entry system

Describes solution, not outcome. Not measurable.

---

**Good:**
> G-002: Enable customers to resolve common issues without human support

Outcome-focused, measurable, doesn't prescribe how.

**Bad:**
> G-002: Implement a chatbot for customer support

Prescribes solution. Conflates means with ends.

### Non-Goals

**Good:**
> Non-goal: Enterprise scale. This system serves small teams (< 50 users).

Clear boundary, prevents scope creep.

**Bad:**
> Non-goal: We won't build bad software.

Not actionable, doesn't exclude anything meaningful.

### Success Metrics

**Good:**
> Customer support tickets decrease by 40% within 6 months of deployment.

Measurable, time-bound, business outcome.

**Bad:**
> Users are satisfied with the system.

Not measurable, subjective.

## Common Mistakes

1. **Vision creep**: Grows to include features, requirements, technical decisions
2. **Unmeasurable goals**: "Improve efficiency" — how much? For whom?
3. **Solution masquerading as problem**: "We need a CRM" vs "Sales can't track interactions"
4. **Missing non-goals**: Scope creeps without explicit exclusions
5. **Changing frequently**: Either too much detail, or still in discovery

## Relationships

- **Vision → Requirements**: Every REQ-XXX traces to at least one G-XXX
- **Vision → Acceptance Tests**: High-level tests verify goals are met
- **Vision → Business Case**: If funding justification needed, Business Case provides financial analysis

## When to Escalate

**Add a Business Case** when:
- Justifying budget or investment to stakeholders
- Competing with other projects for resources
- Need to track ROI or financial metrics
- Enterprise governance requires it

**Add a Stakeholder Map** when:
- Multiple groups with conflicting interests
- Need to manage expectations across departments
- Political complexity in the organisation

## Checklist

- [ ] Problem statement is concrete and stakeholder-focused
- [ ] Goals have unique identifiers (G-001, G-002, ...)
- [ ] Each goal is measurable
- [ ] Non-goals explicitly exclude likely expectations
- [ ] Success metrics are business outcomes, not technical metrics
- [ ] No features, requirements, or technical decisions
- [ ] Target users clearly identified
- [ ] Constraints documented
