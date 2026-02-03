# Entity Model

## Purpose

The Entity Model captures **the core business concepts** in the domain and how they relate. It establishes shared vocabulary and conceptual structure that all stakeholders can understand.

**This is NOT a database schema. It's a conceptual model of the business domain.**

## The Fundamental Distinction

> "A Domain Model is not a data-centric Entity-Relationship Diagram... a domain model does not contain any notion of primary keys, whereas the typical ER diagram does not use inheritance."

The Entity Model describes **what concepts exist in the business**. The database schema describes **how data is stored**. Different concerns.

## Should Contain

### Entities
Core "things" in your domain:
- Have identity (you can distinguish one from another)
- Have a lifecycle (created, change, potentially deleted)
- Are meaningful to the business

Examples: Customer, Order, Product, Agent, Message

### Attributes
Business-relevant properties:
```
Agent
  - name
  - purpose
  - status (active, inactive)
  - createdDate
```

### Relationships
How entities connect:
- **Association**: "Customer places Order"
- **Aggregation**: "Order contains OrderItems"
- **Composition**: "OrderItem cannot exist without Order"
- **Inheritance**: "PremiumCustomer is a type of Customer"

### Cardinality
- One-to-one (1:1)
- One-to-many (1:n)
- Many-to-many (m:n)

Example: "One Customer may have many Orders. Each Order belongs to exactly one Customer."

### Business Rules
Constraints from the domain:
- "An Order must have at least one OrderItem"
- "A Customer cannot have more than 5 active Orders"
- "An Agent must have a purpose"

### Glossary
Definitions of domain terms.

## Should NOT Contain

### Database Details

**Bad:**
```
Customer
  - customer_id: INTEGER PRIMARY KEY AUTO_INCREMENT
  - created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

**Good:**
```
Customer
  - name
  - email
  - registrationDate
```

### Technical Identifiers

**Bad:**
```
Order
  - uuid: UUID
  - version: INTEGER (for optimistic locking)
```

**Good:**
```
Order
  - orderNumber (business identifier)
  - status
  - totalAmount
```

### SQL Data Types

**Bad:**
```
Product
  - price: DECIMAL(10,2)
  - description: VARCHAR(500)
```

**Good:**
```
Product
  - price (monetary amount)
  - description (text)
```

### Indexes and Constraints
```
CREATE INDEX idx_customer_email ON customers(email);
```

### Audit Fields (unless core business requirement)
```
- created_by
- modified_by
- is_deleted
```

### API Structures
```
CustomerDTO
  - id: string
  - _links: { self: string }
```

## Good vs Bad Examples

### Business Concept vs Technical Construct

**Good:**
```
Order
  - orderNumber
  - orderDate
  - status (pending, confirmed, shipped, delivered)
  - totalAmount

  Relationships:
  - placed by: Customer (1)
  - contains: OrderItem (1..n)
  - shipped to: Address (1)
```

**Bad:**
```
orders_table
  - id: BIGINT PK
  - customer_id: BIGINT FK -> customers.id
  - status_code: INT FK -> order_statuses.id
  - total_cents: BIGINT
  - created_at: TIMESTAMP
  - deleted_at: TIMESTAMP NULL
```

### Clear Relationships

**Good:**
```
Agent -- sends --> Message
Agent -- receives --> Message
Agent -- employed by --> Business
```

Relationships named with business verbs.

**Bad:**
```
Agent -- Message (has_many through: agent_messages)
Agent -- Business (belongs_to)
```

ORM terminology instead of business language.

## Common Mistakes

1. **Drawing the database schema**: If you see PKs, FKs, SQL types → wrong level
2. **Missing relationships**: Always ask "How does this entity relate to others?"
3. **Technical entities**: `AuditLog`, `CacheEntry`, `QueueMessage` → infrastructure, not business
4. **Attribute explosion**: Focus on business-essential, not exhaustive
5. **No cardinality**: "Customer has Orders" — but how many?
6. **Implementation inheritance**: `BaseEntity` with `id`, `createdAt` → code pattern, not business concept
7. **Confusing entities and value objects**: Entities have identity; Value Objects have equality by value

## Relationships

- **Requirements → Entity Model**: Requirements imply entities
- **Use Cases → Entity Model**: Entities appear in use cases
- **Entity Model → Architecture**: Entities become components/services
- **Entity Model → Database Schema** (later): Informs but isn't the same

## When to Escalate

**Add a Data Dictionary** when:
- Complex data structures need detailed element-level documentation
- Integration with other systems requires precise data definitions
- Compliance requires data element traceability
- Team needs shared understanding of field meanings and constraints

**Add a Business Rules Document** when:
- Complex business logic spans multiple entities
- Rules need detailed specification beyond entity constraints
- Business analysts need to validate rules independently

**Separate the Glossary** when:
- Glossary grows large (>20 terms)
- Multiple documents reference the same terms
- Non-technical stakeholders need standalone terminology reference

## Checklist

- [ ] Entities represent business concepts, not technical constructs
- [ ] No primary keys or database identifiers
- [ ] No SQL data types
- [ ] No audit fields (unless core requirement)
- [ ] Relationships named with business verbs
- [ ] Cardinality specified for all relationships
- [ ] Attributes are business-relevant
- [ ] Glossary defines key terms
- [ ] Entities mentioned in use cases are present
- [ ] Business rules/constraints documented
