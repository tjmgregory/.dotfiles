# Unified Process Artefact Index

A comprehensive catalogue of all artefacts used across Unified Process variants (RUP, OpenUP, AIUP, AUP). Use this to identify what documents might benefit your project.

## How to Use This Index

1. **Start minimal**: Most projects need only Vision, Requirements, and Acceptance Tests
2. **Add as complexity grows**: When you hit friction, check if an artefact addresses it
3. **Consider project context**: Regulated industries need more; internal tools need less
4. **Tailor, don't adopt wholesale**: UP is a framework, not a checklist

---

## Artefacts by Phase

### Inception Phase

| Artefact | Purpose | When to Use | Source |
|----------|---------|-------------|--------|
| **Vision** | Why we're building this, what success looks like | Always | RUP/AIUP |
| **Business Case** | Financial justification, ROI analysis | Funded projects, enterprise, investor presentations | RUP |
| **Stakeholder Map** | Who cares about this project and why | Multiple stakeholder groups, political complexity | RUP |
| **Risk Register** | Track and mitigate significant unknowns | Complex projects, high uncertainty | RUP/OpenUP |
| **Glossary** | Domain terminology definitions | Complex domains, cross-team communication | RUP |
| **Project Charter** | Formal authorization, scope boundaries | Enterprise projects, governance requirements | RUP |
| **Requirements Catalogue** | What the system must do (functional + non-functional) | Always | AIUP |
| **Test Strategy** | Test levels, types, environments, responsibilities | Projects with QA teams, regulated industries | AIUP |
| **Initial Domain Model** | Preliminary business concept sketch | When domain is unfamiliar to team | RUP |

### Elaboration Phase

| Artefact | Purpose | When to Use | Source |
|----------|---------|-------------|--------|
| **Use Cases** | How actors achieve goals through the system | Always (for functional requirements) | RUP/AIUP |
| **Entity Model** | Core business concepts and relationships | Always | AIUP |
| **Software Architecture Document** | System structure, components, decisions | Always for non-trivial systems | RUP/AIUP |
| **Architecture Decision Records (ADRs)** | Record decisions with rationale | Teams with turnover, long-lived systems | Modern |
| **Supplementary Specifications** | Detailed NFRs, cross-cutting concerns | When NFRs are complex | RUP |
| **Acceptance Tests** | Verify requirements are met | Always | AIUP |
| **API Specification** | OpenAPI/contracts for integrations | Systems with APIs, microservices | Modern |
| **Data Dictionary** | Detailed data element definitions | Data-intensive systems, integrations | RUP |
| **Deployment Diagram** | Infrastructure topology visualization | Distributed systems, DevOps planning | RUP |
| **Use-Case Realization** | How use cases map to design elements | Complex systems, training | RUP |
| **Prototype** | Executable proof of concept | High-risk technical areas, UI validation | RUP |

### Construction Phase

| Artefact | Purpose | When to Use | Source |
|----------|---------|-------------|--------|
| **Iteration Plan** | Plan work for time-boxed iterations | Iterative development (always recommended) | RUP/OpenUP |
| **Sprint/Product Backlog** | Prioritized work items | Agile projects | AUP/Scrum |
| **Integration Build Plan** | How components combine | Multi-component systems | RUP |
| **Test Cases** | Detailed test specifications | Formal testing, regulated industries | RUP |
| **Code** | The implementation | Always | - |
| **Unit/Integration Tests** | Automated verification | Always | - |
| **Definition of Done** | Criteria for completion | Team alignment, quality control | Agile |

### Transition Phase

| Artefact | Purpose | When to Use | Source |
|----------|---------|-------------|--------|
| **Deployment Plan** | How to deploy and configure | Production deployments | RUP |
| **Deployment Runbook** | Step-by-step deployment procedures | Operations teams, complex deployments | Modern |
| **Release Notes** | What changed in this release | External users, compliance | RUP |
| **User Manual** | How to use the system | End-user documentation needed | RUP |
| **Training Materials** | User education resources | User training required | RUP |
| **UAT Results** | User acceptance testing outcomes | Formal acceptance required | RUP |
| **Improvement Log** | Track learnings and feedback | Continuous improvement, retrospectives | Modern |
| **Operations Manual** | How to operate and monitor | Systems requiring operational support | RUP |

---

## Artefacts by Discipline

### Business Modeling

| Artefact | Purpose | When to Use |
|----------|---------|-------------|
| Business Vision | Organization-level goals | Enterprise projects |
| Business Use Cases | How business processes work | Process re-engineering |
| Business Rules Document | Constraints and policies | Complex business logic |
| Business Glossary | Organization terminology | Cross-departmental projects |
| Business Architecture Document | Organization structure, processes | Enterprise architecture |
| Target Organization Assessment | Current vs future state | Transformation projects |

### Requirements

| Artefact | Purpose | When to Use |
|----------|---------|-------------|
| Vision | Project-level goals and scope | Always |
| Requirements Catalogue / SRS | What the system must do | Always |
| Supplementary Specifications | NFRs in detail | Complex quality requirements |
| Use Cases | Actor-goal interactions | Always (functional requirements) |
| Glossary | Domain terms | Complex domains |
| Stakeholder Requests | Raw input from stakeholders | Formal requirements gathering |
| Requirements Attributes | Priority, status, traceability | Large requirements sets |

### Analysis & Design

| Artefact | Purpose | When to Use |
|----------|---------|-------------|
| Software Architecture Document | System structure | Non-trivial systems |
| Architecture Decision Records | Decision rationale | Long-lived systems, team turnover |
| Entity/Domain Model | Business concepts | Always |
| Data Model / Data Dictionary | Data structure details | Data-intensive systems |
| Use-Case Realizations | Design-level use case mapping | Complex systems |
| Interface Specifications | Component contracts | Multi-component systems |
| API Specifications (OpenAPI) | REST API contracts | API-first development |
| Sequence Diagrams | Interaction flows | Complex interactions |
| State Diagrams | State machine behavior | Stateful components |
| Deployment Diagrams | Infrastructure mapping | Distributed systems |

### Implementation

| Artefact | Purpose | When to Use |
|----------|---------|-------------|
| Source Code | The implementation | Always |
| Integration Build Plan | Component integration strategy | Multi-component systems |
| Coding Guidelines | Team standards | Team consistency |

### Test

| Artefact | Purpose | When to Use |
|----------|---------|-------------|
| Test Strategy | Overall test approach | Always (at least informally) |
| Test Plan | Specific test activities | Formal testing phases |
| Acceptance Tests | Business-level verification | Always |
| Test Cases | Detailed test specifications | Formal QA, regulated industries |
| Test Evaluation Summary | Test results analysis | Test phases, releases |
| Defect Reports | Bug tracking | Always (via issue tracker) |

### Deployment

| Artefact | Purpose | When to Use |
|----------|---------|-------------|
| Deployment Plan | Deployment strategy | Production releases |
| Deployment Runbook | Step-by-step procedures | Complex deployments |
| Release Notes | Change documentation | Releases to users |
| Installation Guide | How to install | Distributed software |
| Bill of Materials | Component inventory | Compliance, auditing |

### Configuration & Change Management

| Artefact | Purpose | When to Use |
|----------|---------|-------------|
| Configuration Management Plan | How to manage versions | Formal CM required |
| Change Requests | Proposed changes | Change control process |
| Configuration Audit Results | CM verification | Auditing, compliance |

### Project Management

| Artefact | Purpose | When to Use |
|----------|---------|-------------|
| Software Development Plan | Overall project plan | Formal planning required |
| Iteration Plan | Per-iteration work plan | Iterative development |
| Risk Register | Risk tracking | Complex projects |
| Risk Management Plan | Risk handling approach | High-risk projects |
| Business Case | Project justification | Funded projects |
| Status Assessment | Progress reporting | Stakeholder communication |
| Measurement Plan | Metrics definition | Process improvement |
| Quality Assurance Plan | Quality approach | Regulated industries |
| Problem Resolution Plan | Issue handling | Formal issue management |

### Environment

| Artefact | Purpose | When to Use |
|----------|---------|-------------|
| Development Case | How the team uses UP | Team onboarding, process tailoring |
| Development Environment | Tools, infrastructure | Team setup |
| Guidelines | Specific technique guidance | Team training |

---

## Minimum Artefact Sets by Project Type

### Simple Internal Tool
- Vision (1 paragraph)
- Requirements (bullet list)
- Acceptance Tests (how you know it works)

### Standard Web Application
- Vision
- Requirements Catalogue
- Entity Model
- Use Cases (key flows)
- Software Architecture Document
- Acceptance Tests
- Deployment Plan

### Enterprise System
All of the above, plus:
- Business Case
- Stakeholder Map
- Risk Register
- Supplementary Specifications
- ADRs
- Test Strategy
- Test Plan
- UAT Results
- Operations Manual

### Regulated Industry (Healthcare, Finance, etc.)
All of the above, plus:
- Glossary
- Data Dictionary
- Traceability Matrix
- Configuration Management Plan
- Quality Assurance Plan
- Full Test Documentation
- Audit Trail

### API/Microservices
Standard set, plus:
- API Specification (OpenAPI)
- Interface Specifications
- Deployment Diagrams
- Integration Build Plan

---

## When to Add an Artefact

**Add a Vision** when:
- Project scope is unclear
- Stakeholders have different expectations
- You can't articulate why you're building this

**Add a Business Case** when:
- Justifying budget/investment
- Competing with other projects for resources
- Need to track ROI

**Add a Stakeholder Map** when:
- Multiple groups with different interests
- Political complexity
- Need to manage expectations

**Add a Risk Register** when:
- Significant unknowns
- High-stakes project
- Need to communicate risks to stakeholders

**Add a Glossary** when:
- Team members use terms inconsistently
- Domain is unfamiliar
- Cross-team communication issues

**Add Supplementary Specifications** when:
- Complex NFRs (performance, security, compliance)
- NFRs need more detail than Requirements Catalogue provides
- Architecture decisions need explicit requirements to trace to

**Add ADRs** when:
- Team has turnover
- System will be long-lived
- Need to explain "why we did it this way"

**Add API Specification** when:
- Building APIs for consumers
- Contract-first development
- Multiple teams integrating

**Add a Deployment Runbook** when:
- Complex deployment process
- Operations team different from development team
- Need repeatable, auditable deployments

**Add a Test Strategy** when:
- Multiple test types/levels
- Dedicated QA team
- Need to define test responsibilities

**Add an Iteration Plan** when:
- Working in sprints/iterations
- Need to track progress within phases
- Team coordination required

---

## Sources

- [AIUP (AI Unified Process)](https://aiup.dev/)
- [RUP Artifacts](https://files.defcon.no/RUP/process/artifact/ovu_arts.htm)
- [RUP Templates](https://files.defcon.no/RUP/process/templates.htm)
- [OpenUP (Eclipse)](https://www.eclipse.org/epf/general/OpenUP.pdf)
- [Agile Unified Process](https://en.wikipedia.org/wiki/Agile_unified_process)
- [Architecture Decision Records](https://adr.github.io/)
- [AWS ADR Best Practices](https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/)
