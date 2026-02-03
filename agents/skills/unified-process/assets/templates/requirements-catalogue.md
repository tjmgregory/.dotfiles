# Requirements Catalogue

> **Reminder**: Requirements describe NEEDS, not solutions. "Data must persist durably" (need) vs "Use PostgreSQL" (solution).

## Functional Requirements

<!--
What the system must DO. Each requirement should be:
- Testable (you can verify it works)
- Traceable (links to a goal)
- Solution-neutral (describes WHAT, not HOW)

Good examples:
| REQ-001 | Users can authenticate with existing corporate credentials | G-001 | Must |
| REQ-002 | System maintains complete audit trail of all data changes | G-002 | Must |
| REQ-003 | Users receive notification within 5 minutes of relevant events | G-003 | Should |

Bad examples:
| REQ-001 | Use OAuth 2.0 for login | G-001 | Must | ← Specifies solution
| REQ-002 | Store logs in PostgreSQL | G-002 | Must | ← Technology choice
| REQ-003 | Send push notifications | G-003 | Should | ← Solution, not need
-->

| ID | Requirement | Goal | Priority |
|----|-------------|------|----------|
| REQ-001 | | G-00X | Must/Should/Could |
| REQ-002 | | G-00X | |

<!--
Priority levels (MoSCoW):
- Must: System cannot function without this
- Should: Important but workarounds exist
- Could: Desirable if time permits
- Won't: Explicitly out of scope (for this release)
-->

### Requirement Details

<!--
Expand complex requirements here. Keep the table scannable;
use this section for nuance, edge cases, and acceptance criteria.
-->

#### REQ-XXX: [Title]

**Description**:
<!--
Explain the requirement in full. Include context and rationale.

Example:
"Users must be able to export their data in a standard format. This supports
GDPR Article 20 (right to data portability) and enables users to migrate
to alternative services. The export must include all user-generated content
and associated metadata."
-->

**Acceptance Criteria**:
<!--
How do we know this requirement is satisfied? Be specific and testable.

Example:
- [ ] User can initiate export from account settings
- [ ] Export completes within 24 hours for accounts up to 10GB
- [ ] Export format is documented and machine-readable (JSON/CSV)
- [ ] Export includes all user content, metadata, and activity history
- [ ] User receives notification when export is ready for download
-->

- [ ]
- [ ]

**Open Questions**:
<!--
Unresolved issues that need stakeholder input.

Example:
- Should exported data include content shared by other users?
- What's the retention period for completed exports?
-->

---

## Non-Functional Requirements

<!--
Quality attributes that apply system-wide. These answer "how well" not "what".
Each should be MEASURABLE. Avoid vague terms like "fast" or "secure".

Good examples:
| NFR-001 | Performance | API responses complete within 200ms (95th percentile) | Must |
| NFR-002 | Security | All PII encrypted at rest using industry-standard encryption | Must |
| NFR-003 | Availability | System available 99.9% of time (excludes planned maintenance) | Should |
| NFR-004 | Accessibility | WCAG 2.1 Level AA compliance for all user interfaces | Must |

Bad examples:
| NFR-001 | Performance | System should be fast | Must | ← Not measurable
| NFR-002 | Security | System must be secure | Must | ← Vague
| NFR-003 | Usability | Easy to use | Should | ← Subjective
-->

| ID | Category | Requirement | Priority |
|----|----------|-------------|----------|
| NFR-001 | Performance | | |
| NFR-002 | Security | | |
| NFR-003 | Usability | | |
| NFR-004 | Reliability | | |
| NFR-005 | Scalability | | |

<!--
Common NFR categories (FURPS+):
- Functionality: Security, interoperability
- Usability: Accessibility, learnability, documentation
- Reliability: Availability, fault tolerance, recovery
- Performance: Response time, throughput, capacity
- Supportability: Maintainability, testability, deployability
- +: Constraints, interfaces, legal/regulatory
-->

---

## Constraints

<!--
Fixed limitations that bound the solution space. Unlike requirements
(which describe needs), constraints describe non-negotiable boundaries.

Examples:
- Budget: Maximum $50,000 for infrastructure in year one
- Timeline: Must launch before Q3 regulatory deadline
- Technology: Must integrate with existing SAP system
- Legal: Must comply with GDPR and CCPA
- Team: No machine learning expertise available
-->

-

---

## Assumptions

<!--
Things believed to be true that affect requirements.
Document these so they can be validated and revisited.

Examples:
- Users have modern browsers (Chrome/Firefox/Safari, last 2 versions)
- Peak usage will be weekday business hours (9am-6pm local time)
- Third-party payment API maintains 99.9% availability
- Average user manages fewer than 100 items
-->

-

---

## Traceability

Use these IDs to maintain traceability throughout the project:

- **In Use Cases**: "This use case fulfils REQ-001, REQ-003"
- **In Tests**: "Traces to: REQ-001"
- **In Architecture**: "Component X implements REQ-001"
- **In Tickets**: Reference the ID in ticket title or description

When a requirement changes, search for its ID to find all dependent artefacts.
Changes cascade downward: REQ change → update Use Cases → update Tests → update Code.
