# Requirements Catalogue

## Purpose

The Requirements Catalogue captures **what the system must do** to achieve the Vision goals. Requirements describe needs and capabilities—not solutions or implementations.

**Critical distinction**: Requirements say WHAT, not HOW.

## The Fundamental Rule

> "Requirements describe needs, not solutions."
>
> - **Need**: "Data must be persisted durably"
> - **Solution**: "Use PostgreSQL with replication"

If you're naming technologies, describing data structures, or specifying algorithms, you've crossed into architecture territory.

## Should Contain

### Functional Requirements (REQ-001, REQ-002, ...)
- Unique identifier for traceability
- Traces to at least one Vision goal (G-XXX)
- Testable (you can verify it's satisfied)
- Describes a capability, not an interaction sequence

### Non-Functional Requirements (NFR-001, NFR-002, ...)
Quality attributes:
- Performance (response times, throughput, capacity)
- Security (authentication, authorisation, data protection)
- Reliability (uptime, fault tolerance, recovery)
- Usability (accessibility, learnability)
- Maintainability (modularity, testability)
- Scalability (growth capacity)

### Acceptance Criteria
What conditions must be true for requirement to be satisfied?

### Priority
P1/P2/P3 or MoSCoW.

### Traceability
- Upstream: Which goal(s) it serves
- Downstream: Which use cases exercise it, which tests verify it

### Open Questions
Requirements needing clarification. Unknown requirements are worse than acknowledged gaps.

## Should NOT Contain

- **Solutions**: "Use a message queue" → "Services must communicate asynchronously"
- **Data structures**: "JSON with fields x, y, z" → "Messages must include sender information"
- **UI details**: "Sidebar with navigation links" → "Users must navigate between areas"
- **Technology names**: "Use PostgreSQL" → "Data must persist durably"
- **Use case narratives**: "User clicks, enters, is redirected" → that's a use case

## Good vs Bad Examples

### Testable vs Vague

**Good:**
> REQ-001: All agent communications must be recorded.

Testable, clear.

**Bad:**
> REQ-001: The system should handle communications appropriately.

What is "appropriately"? Untestable.

### Need vs Solution

**Good:**
> REQ-002: Users must be notified of events requiring their attention.

Describes need, doesn't prescribe how.

**Bad:**
> REQ-002: The system shall send email notifications using SendGrid.

Prescribes solution, locks in technology.

### Capability vs Interaction

**Good:**
> REQ-003: The system must support searching historical records.

Describes capability.

**Bad:**
> REQ-003: Users enter search terms in a text field and click Search to query the database.

Describes interaction (use case), mentions implementation (database).

### Measurable NFR

**Good:**
> NFR-001: The system must respond to user queries within 200ms at the 95th percentile.

Specific, measurable, testable.

**Bad:**
> NFR-001: The system should be fast.

What is "fast"? Useless.

## Common Mistakes

1. **Sneaking in architecture**: Watch for technology names, data formats, protocols
2. **Writing use cases as requirements**: If it reads like a story with steps, it's a use case
3. **Untestable requirements**: Subjective terms without criteria
4. **Missing traceability**: Orphan requirements suggest scope creep
5. **Premature specificity**: If only one implementation is possible, you've embedded a solution
6. **Confusing functional/non-functional**: Functional = WHAT it does; NFR = HOW WELL

## The Use Case Distinction

**Requirements** define capabilities: "The system must support X."
**Use Cases** describe interactions: "The user does A, then B happens."

They're complementary, not interchangeable:
- Use cases elaborate HOW requirements are fulfilled through specific scenarios
- Use cases cannot capture complex business rules, performance requirements, or non-process aspects
- A requirement like "Users must authenticate" becomes a use case "User Logs In" showing the flow

**When to use both**: Use cases are derived from requirements and provide usage context. The Requirements Catalogue is broader—it includes everything the system must do, while use cases focus on actor-goal interactions.

## When to Escalate

**Add Supplementary Specifications** when:
- NFRs need more detail than fits in this document
- Complex FURPS+ requirements (Functionality, Usability, Reliability, Performance, Supportability)
- Regulatory or compliance requirements need elaboration
- Cross-cutting concerns apply system-wide

**Add a Glossary** when:
- Team uses domain terms inconsistently
- Requirements reference concepts that need definition
- Stakeholders have different interpretations of terms

## Relationships

- **Vision → Requirements**: Every REQ-XXX references at least one G-XXX
- **Requirements → Use Cases**: UC-XXX indicates which REQ-XXX it exercises
- **Requirements → Acceptance Tests**: TC-XXX references which REQ-XXX it validates
- **Requirements → Architecture**: "We chose X because it satisfies REQ-XXX"

## Checklist

- [ ] Each requirement has unique identifier (REQ-XXX, NFR-XXX)
- [ ] Each requirement traces to at least one goal (G-XXX)
- [ ] Each requirement is testable
- [ ] No technology names or product names
- [ ] No data structures or formats specified
- [ ] No UI details
- [ ] No interaction sequences (those are use cases)
- [ ] NFRs have measurable criteria
- [ ] Open questions flagged, not hidden
- [ ] Priority indicated
