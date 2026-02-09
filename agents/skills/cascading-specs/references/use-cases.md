# Use Cases

## Purpose

Use Cases describe **how actors interact with the system to achieve their goals**. They bridge abstract requirements and concrete implementation by showing interaction flows.

## The Fundamental Principle

> **Use cases are goal-oriented, not function-oriented.**

A use case describes what an actor is trying to ACHIEVE, not what functions the system provides.

- **Good**: "Customer Purchases Product" (actor's goal)
- **Bad**: "Process Payment" (system function)

The name should reflect what the ACTOR wants, not what the SYSTEM does.

## Should Contain

### Use Case Identifier
UC-001, UC-002, ...

### Title
Actor's goal in verb-noun format:
- "Customer Places Order"
- "Admin Configures System"
- "Agent Sends Message"

### Actor
External to the system:
- Human users (Customer, Admin, Operator)
- External systems (Payment Gateway, Email Service)
- Time (for scheduled operations)

### Preconditions
What must be true BEFORE:
- "User is authenticated"
- "Shopping cart contains at least one item"

### Postconditions
What is true AFTER successful completion:
- "Order is recorded in the system"
- "Confirmation email has been sent"

### Main Success Scenario
The "happy path"—numbered steps showing interaction when everything goes right:

```
1. Customer selects items to purchase
2. System displays order summary with total
3. Customer provides payment information
4. System validates payment
5. System records the order
6. System sends confirmation to customer
```

Steps should be:
- Observable (you can see it happen)
- At the right granularity
- Alternating between actor and system

### Extensions (Alternative Flows)
What happens when things go differently:

```
4a. Payment validation fails:
    4a1. System displays error message
    4a2. Customer corrects payment information
    4a3. Resume at step 4

3a. Customer cancels:
    3a1. System discards order
    3a2. Use case ends
```

### Requirement Traceability
Which requirements does this fulfil? (REQ-001, REQ-003, ...)

## Should NOT Contain

### User Interface Details

**Bad:**
> 3. Customer clicks the blue "Checkout" button in the top-right corner

**Good:**
> 3. Customer initiates checkout

### Implementation Details

**Bad:**
> 4. System executes SQL query to check inventory

**Good:**
> 4. System verifies item availability

### Internal System Processing

**Bad:**
> 5. System calculates tax using TaxCalculator service, applies discounts from PromotionEngine

**Good:**
> 5. System calculates order total including applicable taxes and discounts

### Non-Functional Requirements

**Bad:**
> 6. System responds within 200ms

Performance requirements belong in Requirements Catalogue.

### Data Structures

**Bad:**
> 7. System returns JSON object: { orderId: string, status: "confirmed" }

## Goal Levels

### Summary Level (+)
High-level goals spanning multiple sessions or actors. Decompose into user-goal use cases.
Example: "Customer Manages Account"

### User Goal Level (!)
**Most important.** A complete goal an actor achieves in one session. Actor would say "I'm done" when this completes.
Examples: "Customer Places Order", "Admin Creates User"

### Subfunction Level (-)
Part of achieving a larger goal. Extract when multiple use cases share substeps.
Example: "System Validates Payment"

## Good vs Bad Examples

### Goal-Focused vs Function-Focused

**Good:**
> UC-001: Customer Purchases Product
> Actor: Customer
> Goal: Acquire a product from the store

Focus on what the ACTOR wants.

**Bad:**
> UC-001: Process Order
> Actor: System
> Goal: Execute order processing workflow

"System" is not an actor. "Process Order" is a function.

### Appropriate Detail vs Too Much UI

**Good:**
```
1. Customer indicates intent to check out
2. System displays order summary
3. Customer provides shipping address
4. Customer provides payment information
5. System processes payment
6. System confirms order
```

**Bad:**
```
1. Customer clicks "Cart" icon (top-right, badge shows count)
2. Customer clicks "Proceed to Checkout" button (green, below items)
3. Customer fills in shipping form (name, address, city, zip, country dropdowns)
4. Customer clicks "Continue to Payment"
5. Customer enters credit card number in 16-digit field with Luhn validation
```

The bad example is a UI specification.

## Common Mistakes

1. **CRUD use cases**: "Create Customer", "Read Customer" → database operations, not user goals
2. **System as actor**: The system is what we're building, not an actor
3. **Function names as titles**: "ValidateInput", "CalculateTotal" → functions, not goals
4. **Missing actor goals**: Every use case should answer "Why does the actor care?"
5. **Mixing levels**: Don't mix summary and subfunction steps
6. **No alternative flows**: Happy path only is incomplete
7. **Too much internal detail**: If the actor can't observe it, it doesn't belong

## Relationships

- **Requirements → Use Cases**: Use cases fulfil requirements
- **Use Cases → Acceptance Tests**: Scenarios become test scenarios
- **Use Cases → Entity Model**: Entities mentioned should appear in model
- **Use Cases → Architecture**: Architecture must support use cases

## When to Escalate

**Extract a Subfunction Use Case** when:
- The same steps appear in multiple use cases
- A step is complex enough to warrant its own specification
- You need to specify details of a validation or process shared across use cases

**Add Use-Case Realizations** when:
- Need to show how use cases map to design elements
- Training new team members on system structure
- Complex interactions need design-level documentation

## Checklist

- [ ] Has unique identifier (UC-XXX)
- [ ] Title is actor's goal in verb-noun format
- [ ] Actor is external (not "System")
- [ ] Preconditions state what must be true before
- [ ] Postconditions state what's true after success
- [ ] Main scenario has numbered steps
- [ ] Steps alternate between actor and system appropriately
- [ ] Steps are observable (no internal processing)
- [ ] No UI details (buttons, forms, layouts)
- [ ] No implementation details (databases, APIs)
- [ ] Extensions cover error conditions
- [ ] Requirements traceability documented
- [ ] Goal level appropriate (usually user-goal)
