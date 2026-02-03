# Supplementary Specifications

## Purpose

Supplementary Specifications capture **requirements that don't fit naturally into use cases**. Primarily non-functional requirements (NFRs) and cross-cutting concerns that apply system-wide.

## The Fundamental Principle

> Use Cases + Supplementary Specifications = Complete Requirements

Use cases capture WHAT the system does (functional behaviour).
Supplementary Specifications capture HOW WELL it does it (quality attributes, constraints).

If a requirement applies to a specific interaction → probably belongs in a use case.
If a requirement applies system-wide → probably belongs here.

## Should Contain

### Performance
Response times, throughput, capacity:
```
PERF-001: API response time
  - 95th percentile < 200ms for read operations
  - 95th percentile < 500ms for write operations
  - Measured under normal load (1000 concurrent users)
```

### Scalability
Growth capacity:
```
SCALE-001: User capacity
  - Support 10,000 registered users
  - Support 1,000 concurrent active users
  - Horizontal scaling to 5x without architecture changes
```

### Reliability / Availability
Uptime, fault tolerance:
```
REL-001: Availability
  - 99.9% uptime (8.76 hours downtime per year maximum)
  - Planned maintenance windows: Sundays 02:00-04:00 UTC

REL-002: Fault tolerance
  - Single component failure must not cause system-wide outage
  - Recovery time < 5 minutes
```

### Security
Authentication, authorisation, data protection:
```
SEC-001: Authentication
  - All users must authenticate before protected resources
  - Session timeout after 30 minutes of inactivity
  - Support multi-factor authentication
```

### Usability
Accessibility, learnability:
```
USE-001: Accessibility
  - WCAG 2.1 Level AA compliance
  - Keyboard navigation for all functions
  - Screen reader compatible
```

### Maintainability
Modularity, testability, deployability:
```
MAINT-001: Deployability
  - Zero-downtime deployments
  - Rollback capability within 5 minutes
  - Automated deployment pipeline
```

### Design Constraints
```
CONST-001: Technology stack
  - Backend: Python 3.11+
  - Database: PostgreSQL 14+
  - Rationale: Existing team expertise
```

### Legal and Regulatory
```
LEGAL-001: GDPR compliance
  - Right to access: Users can export their data
  - Right to erasure: Users can request deletion
  - Data processing records maintained
```

### Standards
```
STD-001: API standards
  - RESTful design following OpenAPI 3.0
  - JSON:API specification for response format
```

## Should NOT Contain

### Functional Requirements

**Bad:**
> The system shall allow users to create orders.

Functional—belongs in use case or requirements catalogue.

### Use Case Details

**Bad:**
> When the user clicks Submit, the system validates the form.

Interaction sequence—belongs in use case.

### Architecture Decisions

**Bad:**
> The system shall use microservices architecture.

Architecture—belongs in SAD. Supplementary Specs might constrain ("must be horizontally scalable") but don't prescribe how.

### Implementation Details

**Bad:**
> The system shall use Redis for caching with TTL of 300 seconds.

Too specific. Requirement might be "frequently accessed data should be cached for performance."

## Good vs Bad Examples

### Measurable vs Vague

**Good:**
```
PERF-001: Search response time
  - Simple searches: 500ms (95th percentile)
  - Complex searches: 2 seconds (95th percentile)
  - Measured with production-representative data
```

**Bad:**
> PERF-001: The system should be fast.

### Constraint vs Solution

**Good:**
```
SEC-001: Data encryption
  - All PII must be encrypted at rest
  - Encryption must use industry-standard algorithms
```

States the NEED.

**Bad:**
```
SEC-001: Data encryption
  - Use AES-256-GCM for all encryption
  - Keys stored in AWS KMS in us-east-1
  - Key rotation every 90 days via Lambda
```

Implementation specification.

### Cross-Cutting vs Specific

**Good:**
```
LOG-001: Logging requirements
  - All API requests must be logged
  - Logs must include: timestamp, user ID, action, result
  - Logs must not contain passwords or tokens
  - Log retention: 90 days online, 2 years archived
```

System-wide—appropriate.

**Bad:**
```
LOG-001: Order creation logging
  - When order created, log details
  - Include customer name and items
```

Specific to one function—belongs in use case or specific requirement.

## FURPS+ Categories

Checklist framework:

| Category | Covers |
|----------|--------|
| **F**unctionality | Features, security, interoperability |
| **U**sability | Human factors, accessibility, documentation |
| **R**eliability | Availability, failure handling, recovery |
| **P**erformance | Speed, throughput, capacity, scalability |
| **S**upportability | Maintainability, testability, deployability |
| **+** | Constraints, interfaces, legal, standards |

## Common Mistakes

1. **Unmeasurable requirements**: "Secure" — against what? Measured how?
2. **Requirements without rationale**: WHY is 99.9% uptime required?
3. **Contradictory requirements**: 100ms response AND external service that takes 200ms
4. **Gold plating**: 99.99% uptime is much harder than 99.9% — really needed?
5. **Missing categories**: Only performance, ignoring security/usability
6. **Implementation disguised as requirements**: Technology names = crossed the line

## Relationships

- **Vision → Supplementary Specifications**: Success metrics and constraints inform NFRs
- **Supplementary Specifications → Architecture**: Architecture must address NFRs
- **Supplementary Specifications → Acceptance Tests**: NFRs need verification
- **Use Cases + Supplementary Specifications**: Together = complete requirements

## When This Document Isn't Needed

For simple projects, NFRs can stay in the Requirements Catalogue. Use a separate Supplementary Specifications document when:
- NFRs are numerous or complex
- Different stakeholders care about different NFR categories
- Compliance requires detailed NFR traceability
- Architecture decisions need explicit NFR references

## Related Artefacts

**Risk Register**: If NFRs imply significant risk, track them in a Risk Register.

**Operations Manual**: Operational NFRs (monitoring, alerting, recovery) may inform Operations Manual content.

**Service Level Objectives (SLOs)**: Modern alternative for performance/availability requirements, especially in DevOps contexts.

## Checklist

- [ ] Requirements have unique identifiers
- [ ] Each requirement is measurable/testable
- [ ] All FURPS+ categories considered
- [ ] No functional requirements (those go elsewhere)
- [ ] No architecture decisions (those go in SAD)
- [ ] Rationale provided for significant requirements
- [ ] No contradictions between requirements
- [ ] Requirements are achievable (not gold-plated)
- [ ] Legal/regulatory requirements identified
- [ ] Design constraints documented
- [ ] Interface requirements captured
