# Acceptance Tests

## Purpose

Acceptance Tests define **how we verify that requirements are met**. They answer: "How do we know the system is working correctly from a business perspective?"

Acceptance tests are **black-box** and **business-focused**. They test observable behaviour, not internal implementation.

## The Fundamental Principle

> Acceptance tests verify WHAT the system does, not HOW it does it.

An acceptance test should:
- Be understandable by non-technical stakeholders
- Test behaviour visible to users/actors
- Pass or fail based on business criteria
- Remain valid even if implementation changes

## Should Contain

### Test Case Identifier
TC-001, TC-002, ...

### Title
What behaviour is being tested:
- "Verify customer can place order"
- "Verify payment failure is handled gracefully"

### Traceability
Which requirement(s) or use case(s) does this verify?
- Traces to: REQ-001, UC-003

### Preconditions
System state before the test:
- "Customer is logged in"
- "Shopping cart contains 2 items"

### Test Steps
Actions in business language:
```
1. Customer initiates checkout
2. Customer provides valid shipping address
3. Customer provides valid payment information
4. Customer confirms order
```

### Expected Results
Observable outcomes:
```
- Order is created with status "confirmed"
- Order appears in customer's order history
- Confirmation is sent to customer
```

### Pass/Fail Criteria
Clear, unambiguous conditions.

## Should NOT Contain

### Implementation Details

**Bad:**
> Expected: Database contains row in orders table with customer_id = 123

**Good:**
> Expected: Order appears in customer's order history

### Internal System State

**Bad:**
> Verify: OrderService.orderCache contains order ID

### Technical Assertions

**Bad:**
```
Assert: response.statusCode == 200
Assert: response.body.orderId matches UUID pattern
```

This is API testing, not acceptance testing.

### Unit Test Details

**Bad:**
> Test: OrderValidator.validate() returns true for valid order

### Performance Metrics

**Bad:**
> Verify: Response time < 200ms

Performance testing is separate.

## Good vs Bad Examples

### Business Language vs Technical Language

**Good:**
```
TC-001: Customer successfully places order

Preconditions:
- Customer is logged in
- Cart contains items

Steps:
1. Customer proceeds to checkout
2. Customer enters shipping address
3. Customer enters payment details
4. Customer confirms order

Expected:
- Order confirmation is displayed
- Order appears in customer's order history
- Confirmation email is received
```

**Bad:**
```
TC-001: POST /api/orders returns 201

Preconditions:
- Valid JWT token in Authorization header
- Request body: { "items": [...], "shippingAddress": {...} }

Steps:
1. Send POST request to /api/orders
2. Parse response JSON
3. Query GET /api/orders/{id}

Expected:
- Response status: 201 Created
- Response body contains orderId (UUID)
```

The bad example is an API test.

### Observable Behaviour vs Internal State

**Good:**
```
TC-002: Agent messages are recorded for audit

Steps:
1. Agent A sends message to Agent B
2. Query audit log for recent activity

Expected:
- Audit log contains entry for the message
- Entry shows sender, recipient, timestamp, content
```

**Bad:**
```
TC-002: MessageRepository persists messages

Steps:
1. Call messageRepository.save(message)
2. Query: SELECT * FROM messages WHERE id = ?

Expected:
- Row exists with correct sender_id, recipient_id
```

Tests implementation, not business requirement.

## Given-When-Then Format

Popular BDD/Gherkin format:

```
TC-001: Customer places order successfully

Given:
  - Customer is logged in
  - Cart contains 2 items totalling $50

When:
  - Customer completes checkout with valid payment

Then:
  - Order is created with status "confirmed"
  - Order total is $50 plus applicable tax
  - Customer receives confirmation email
```

## Test Derivation

### From Requirements
Each requirement should have at least one test:

```
REQ-001: Users must authenticate before accessing protected resources

→ TC-010: Unauthenticated user cannot access dashboard
→ TC-011: Authenticated user can access dashboard
→ TC-012: Expired session redirects to login
```

### From Use Cases
Each scenario (main + extensions) should have tests:

```
UC-001: Customer Places Order
  Main Success → TC-001: Successful order placement
  Extension 4a (payment fails) → TC-002: Payment failure handled
  Extension 3a (address invalid) → TC-003: Invalid address rejected
```

## Common Mistakes

1. **Testing implementation, not behaviour**: Would fail after refactoring that doesn't change behaviour
2. **Technical language**: Non-technical stakeholders can't understand
3. **No traceability**: Tests that don't link to requirements
4. **Missing negative cases**: Only happy paths
5. **Vague expected results**: "System handles it correctly"
6. **Overlap with unit tests**: Acceptance tests are end-to-end
7. **Environment dependencies**: Only pass in specific environments

## Relationships

- **Requirements → Acceptance Tests**: Tests verify requirements
- **Use Cases → Acceptance Tests**: Scenarios become test scenarios
- **Acceptance Tests → Code**: Code must pass tests
- **Acceptance Tests ↔ QA**: Define "done" from business perspective

## When to Escalate

**Add a Test Strategy** when:
- Multiple test types/levels (unit, integration, E2E, performance)
- Dedicated QA team needs guidance
- Need to define test responsibilities across teams
- Regulated industry requires documented test approach

**Add a Test Plan** when:
- Specific testing phase needs detailed planning
- Resources, schedule, and scope need formal definition
- Stakeholders need visibility into test activities

**Add UAT (User Acceptance Testing) Documentation** when:
- Formal user sign-off required before release
- Business users will perform acceptance testing
- Entry/exit criteria need explicit definition
- Compliance requires documented user acceptance

**UAT Entry Criteria** (must be met before UAT begins):
- All functional requirements implemented
- QA testing complete, critical bugs fixed
- Test environment matches production
- Test data prepared

**UAT Exit Criteria** (must be met for sign-off):
- All acceptance tests pass
- No critical defects open
- Stakeholders formally approve

## Checklist

- [ ] Each test has unique identifier (TC-XXX)
- [ ] Each test traces to requirement(s) or use case(s)
- [ ] Preconditions clearly stated
- [ ] Steps use business language, not technical
- [ ] Expected results are observable behaviours
- [ ] Pass/fail criteria are unambiguous
- [ ] No implementation details (databases, APIs, code)
- [ ] Non-technical stakeholders can understand
- [ ] Negative cases (errors, failures) covered
- [ ] Tests are reproducible
