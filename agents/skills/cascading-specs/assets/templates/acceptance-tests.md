# Acceptance Tests

> **Reminder**: Acceptance tests verify BUSINESS behaviour, not technical implementation. If a non-technical stakeholder can't understand the test, it's too technical.

<!--
Acceptance tests answer: "How do we know the system is working correctly from a BUSINESS perspective?"

Key principles:
- Black-box: Test observable behaviour, not internal implementation
- Business language: Steps a stakeholder can understand
- Stable: Should pass even if implementation is refactored
-->

## TC-001: [Behaviour being tested - in business terms]

<!--
Good titles:
- TC-001: Customer successfully places order
- TC-002: Payment failure displays helpful error
- TC-003: Expired session redirects to login

Bad titles:
- TC-001: POST /api/orders returns 201 ← API test, not acceptance test
- TC-002: OrderService.create() works ← Unit test
- TC-003: Test the checkout ← Vague
-->

**Traces to**: REQ-XXX, UC-XXX

<!--
Link to requirements and use cases this test verifies.
Every requirement should have at least one acceptance test.
Every use case scenario (main + extensions) should have tests.
-->

**Preconditions**:
<!--
System state BEFORE the test begins. Written in business terms.

Good preconditions:
- Customer is logged in with a verified account
- Shopping cart contains 2 items totalling $50
- Customer has a valid saved payment method

Bad preconditions:
- Database seeded with test data ← Technical detail
- JWT token in Authorization header ← Implementation detail
- Redis cache cleared ← Infrastructure concern
-->

- [ ] [System state in business terms]
- [ ] [Required setup in business terms]

**Steps**:
<!--
Actions in BUSINESS language. Describe intent, not mechanics.

Good steps:
1. Customer proceeds to checkout
2. Customer confirms shipping address
3. Customer selects standard shipping
4. Customer completes payment

Bad steps:
1. Click the "Checkout" button ← UI mechanics
2. POST /api/checkout with body {...} ← API details
3. Assert response status is 200 ← Technical assertion
-->

1. [Action in business language]
2. [Action in business language]
3. [Action in business language]

**Expected Results**:
<!--
Observable outcomes in business terms. What can a user SEE or VERIFY?

Good expected results:
- Order confirmation is displayed with order number
- Order appears in customer's order history
- Confirmation email is received within 5 minutes
- Inventory is reduced by ordered quantity

Bad expected results:
- Database contains row in orders table ← Implementation detail
- Response JSON includes orderId field ← API format
- OrderCreatedEvent is published to queue ← Infrastructure
-->

- [ ] [Observable outcome in business terms]
- [ ] [Observable outcome in business terms]

**Pass/Fail Criteria**:
- Pass: All expected results observed
- Fail: Any expected result not observed

---

## TC-002: [Behaviour being tested - negative case]

<!--
Don't just test happy paths. Test failures, errors, and edge cases.

Examples of negative test cases:
- Payment method declined
- Required field missing
- Session expired
- Insufficient inventory
- Duplicate submission
-->

**Traces to**: REQ-XXX, UC-XXX (extension Xa)

### Given-When-Then Format

<!--
BDD/Gherkin style - excellent for stakeholder communication.
-->

**Given**:
<!--
Context and preconditions. Sets up the scenario.

Example:
- Customer is logged in
- Cart contains 1 item priced at $100
- Customer's saved payment method has expired
-->

- [Precondition]
- [Precondition]

**When**:
<!--
The action being tested. Usually a single action.

Example:
- Customer attempts to complete checkout using saved payment method
-->

- [Action]

**Then**:
<!--
Expected outcomes. What should happen as a result.

Example:
- Customer is informed that payment method has expired
- Customer is prompted to update payment information
- Order is NOT created
- Cart contents are preserved
-->

- [Expected outcome]
- [Expected outcome]

---

## TC-003: [Edge case or boundary condition]

<!--
Test boundaries and edge cases that might be overlooked.

Examples:
- Order with exactly the minimum allowed quantity
- Order at the maximum allowed value
- Customer with no order history
- Action at session timeout boundary
- Concurrent updates to the same resource
-->

**Traces to**: REQ-XXX

**Given**:
- [Boundary condition setup]

**When**:
- [Action at boundary]

**Then**:
- [Expected behaviour at boundary]

---

## Test Coverage Matrix

<!--
Ensures every requirement and use case scenario has test coverage.
Review this table to identify gaps.

For use cases, test:
- Main success scenario
- Each extension/alternative flow
- Error conditions
-->

| Requirement / Scenario | Test Cases | Status |
|------------------------|------------|--------|
| REQ-001: [Brief description] | TC-001 | ☐ |
| REQ-002: [Brief description] | TC-002, TC-003 | ☐ |
| UC-001 Main Success | TC-001 | ☐ |
| UC-001 Extension 3a | TC-004 | ☐ |
| UC-001 Extension 6a | TC-002 | ☐ |

<!--
Status options:
☐ - Not yet executed
☑ - Passed
☒ - Failed
⊘ - Blocked/Cannot execute
-->

---

## Test Data Requirements

<!--
Optional: Document test data needed for acceptance testing.
Focus on BUSINESS scenarios, not technical setup.

Example:
- Customer with verified account and order history
- Customer with verified account and no orders
- Customer with payment method on file
- Customer with expired payment method
- Products with various stock levels (in stock, low stock, out of stock)
- Products with different shipping requirements (standard, oversized, hazardous)
-->
