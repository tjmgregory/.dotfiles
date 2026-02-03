# Software Architecture Document

## Purpose

The Software Architecture Document (SAD) describes **how the system is structured** to meet requirements. It captures significant architectural decisions, rationale, and component interactions.

## The Fundamental Principle

> Architecture is about STRUCTURE and DECISIONS, not implementation details.

The SAD answers:
- What are the major components?
- What are their responsibilities?
- How do they interact?
- Why these choices over alternatives?

It does NOT contain:
- Code
- Detailed algorithms
- Class-level design

## Should Contain

### Architectural Views

#### Use-Case View (Mandatory)
How architecture supports key use cases. Trace architecturally significant use cases through components.

"When UC-001 executes: API Gateway → Order Service → Payment Service → Database"

#### Logical View (Mandatory)
Major components and responsibilities:

```
API Gateway
  - Responsibility: Route requests, handle authentication
  - Interfaces: HTTP REST

Order Service
  - Responsibility: Manage order lifecycle
  - Interfaces: Internal API, Message Queue
```

#### Process View (If Multi-Threaded/Distributed)
Concurrency, processes, threads, synchronisation.

#### Deployment View (If Distributed)
How components deploy to infrastructure, network topology, scaling.

#### Implementation View (If Differs from Design)
Code organisation, module structure, key libraries.

### Architectural Decisions (ADRs)

```
ADR-001: Use Event Sourcing for Order State

Context: Orders go through many state changes needing audit.

Decision: Store orders as event sequence rather than current state.

Rationale:
- Supports REQ-003 (complete audit trail)
- Enables replay and debugging
- Aligns with eventual consistency model

Consequences:
- More complex querying (need projections)
- Storage grows over time
- Team needs event sourcing experience
```

### Quality Attribute Handling

| NFR | Architectural Approach |
|-----|----------------------|
| NFR-001: 200ms response time | Caching layer, async processing |
| NFR-002: 99.9% availability | Redundant services, failover |

### Component Interfaces
- Synchronous (HTTP, gRPC)
- Asynchronous (message queues, events)
- Data formats

### Dependencies
External systems, libraries, services.

## Should NOT Contain

### Code

**Bad:**
```python
class OrderService:
    def __init__(self, repository, payment_client):
        self.repository = repository
```

### Detailed Algorithms

**Bad:**
> The recommendation engine uses collaborative filtering with cosine similarity threshold of 0.7, implemented using sparse matrix multiplication...

### Database Schemas

**Bad:**
```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id)
);
```

The SAD might mention "PostgreSQL for persistence" but not the schema.

### Requirements or Use Cases
These are INPUT to architecture, not content.

## Good vs Bad Examples

### Component Description

**Good:**
```
Message Broker
  Responsibility: Decouple services through asynchronous messaging
  Interfaces:
    - Publish: Services send messages to topics
    - Subscribe: Services receive messages from topics
  Technology: RabbitMQ
  Rationale: Need reliable message delivery with acknowledgment (REQ-005)
```

**Bad:**
```
RabbitMQ
  - Install RabbitMQ 3.9.x
  - Configure exchange type: topic
  - Set prefetch count to 10
  - Queue TTL: 24 hours
```

Operational configuration, not architecture.

### Architectural Decision

**Good:**
```
ADR-002: Separate Read and Write Models (CQRS)

Context:
Read and write patterns differ significantly.

Decision:
Commands go through domain model. Queries use optimised read projections.

Alternatives Considered:
1. Single model with caching - rejected (cache invalidation complexity)
2. Single model with read replicas - rejected (query flexibility limited)

Consequences:
- Eventual consistency between models
- Need to maintain projections
- Simpler scaling of reads
```

**Bad:**
> We're using CQRS because it's a modern pattern.

No context, rationale, alternatives, or consequences.

### Quality Attribute Mapping

**Good:**
```
Scalability (NFR-004: Support 10,000 concurrent users)

Approach:
- Stateless services enable horizontal scaling
- Load balancer distributes traffic
- Database read replicas handle query load

Verification:
Load testing with 15,000 users: 180ms response, 0.01% error rate
```

**Bad:**
> The system will be scalable.

## Common Mistakes

1. **No rationale**: Listing technologies without explaining WHY
2. **Too much detail**: Code, schemas, configuration
3. **No quality attribute coverage**: Ignoring how architecture addresses NFRs
4. **Ivory tower**: Idealised version that doesn't match reality
5. **Missing dependencies**: External systems not documented
6. **No traceability**: Can't explain how architecture supports requirements
7. **Outdated**: Doesn't match actual system

## Relationships

- **Requirements → Architecture**: Architecture addresses requirements with traceability
- **Use Cases → Architecture**: Shows how key use cases are supported
- **Entity Model → Architecture**: Entities inform service boundaries
- **Architecture → Code**: Code should conform
- **Architecture → Deployment**: Logical to physical mapping

## When to Escalate

**Use Separate ADR Files** when:
- Many architectural decisions accumulate
- Decisions need detailed context that clutters the SAD
- Team turnover requires preserved decision history
- Store as `docs/adr/ADR-001-title.md` files

**Add an API Specification (OpenAPI)** when:
- Building APIs for external or internal consumers
- Multiple teams need to integrate
- Contract-first development approach
- API documentation needs to stay current with implementation

**Add a Deployment Diagram** when:
- System is distributed across multiple nodes
- Infrastructure topology is non-obvious
- DevOps team needs visual reference
- Planning capacity or failover

**Add a Data Dictionary** when:
- Complex data structures need detailed documentation
- Integration with other systems requires precise data definitions
- Compliance requires data element traceability

## Checklist

- [ ] Major components identified with responsibilities
- [ ] Component interfaces defined
- [ ] Significant decisions have rationale (ADRs)
- [ ] Quality attributes (NFRs) addressed
- [ ] Key use cases can be traced through
- [ ] External dependencies documented
- [ ] No code or implementation details
- [ ] No database schemas
- [ ] Alternatives considered are documented
- [ ] Technology choices justified
- [ ] Deployment approach described (if distributed)
