# UC-XXX: [Actor's Goal in Verb-Noun Format]

<!--
Use case titles should describe the ACTOR'S GOAL, not a system function.

Good titles:
- UC-001: Customer Places Order
- UC-002: Agent Reviews Application
- UC-003: Manager Approves Expense

Bad titles:
- UC-001: Order Processing ← System function, not actor goal
- UC-002: Application Review Screen ← UI element
- UC-003: Handle Expense ← Vague, passive
-->

## Summary

| Field | Value |
|-------|-------|
| **Actor** | |
| **Goal** | |
| **Level** | User Goal |
| **Traces to** | REQ-XXX, REQ-XXX |

<!--
ACTOR: Who initiates this use case. Must be external to the system.
  Good: Customer, Support Agent, External Payment System
  Bad: "The system", "OrderService", "Database"

GOAL: What the actor is trying to achieve. Should be a complete sentence.
  Good: "Successfully purchase items in shopping cart"
  Bad: "Process order" (vague), "Click checkout button" (UI action)

LEVEL: Determines scope and granularity
  - Summary: High-level business process (spans hours/days, multiple sessions)
    Example: "Customer Completes Return Process"
  - User Goal: Primary level. One sitting, one actor, one goal (most common)
    Example: "Customer Places Order"
  - Subfunction: Supporting functionality called by other use cases
    Example: "System Validates Address"
-->

## Preconditions

<!--
What must be TRUE before this use case can begin.
These are not steps—they are state that already exists.

Good examples:
- Customer is authenticated
- Shopping cart contains at least one item
- Customer has a valid payment method on file

Bad examples:
- Customer logs in ← This is a step, not a precondition
- Customer adds items to cart ← This is another use case
-->

- [ ]
- [ ]

## Postconditions

<!--
What is TRUE after successful completion.
Describes the new state of the world, not actions taken.

Good examples:
- Order exists with status "confirmed"
- Inventory reduced by ordered quantities
- Customer has received confirmation email

Bad examples:
- Email was sent ← Describes action, not resulting state
- Order is processed ← Vague
-->

- [ ]
- [ ]

## Main Success Scenario

<!--
The "happy path"—when everything goes well.
Each step is EITHER an actor action OR a system response. Alternate between them.

CRITICAL RULES:
1. Use business language, not UI language
   Good: "Customer provides shipping address"
   Bad: "Customer fills in address form and clicks Next button"

2. Focus on INTENT, not mechanics
   Good: "Customer selects payment method"
   Bad: "Customer clicks the dropdown menu labeled 'Payment'"

3. System responses describe WHAT happens, not HOW
   Good: "System validates payment information"
   Bad: "System calls PaymentGateway.validate() and checks response code"

4. Each step should advance toward the goal
   Bad: "System displays loading spinner" ← Doesn't advance goal

Example Main Success Scenario:
1. Customer initiates checkout
2. System displays order summary with items and totals
3. Customer confirms or modifies shipping address
4. System displays available shipping options with costs
5. Customer selects shipping method
6. Customer provides payment information
7. System validates payment and authorises charge
8. System creates order and reserves inventory
9. System displays confirmation with order number
10. System sends confirmation email to customer
-->

1. [Actor action]
2. System [response]
3. [Actor action]
4. System [response]
5. ...

## Extensions

<!--
What happens when things go differently. These handle:
- Errors and failures
- Alternative choices
- Edge cases
- Business rule violations

Format: [Step number][letter]. [Condition]:
The number refers to the main scenario step where this branches.

Example Extensions:
3a. Shipping address is invalid:
    3a1. System highlights invalid fields and explains requirements
    3a2. Customer corrects address
    3a3. Resume at step 3

6a. Payment method is declined:
    6a1. System informs customer of decline (without exposing sensitive details)
    6a2. Customer provides alternative payment method
    6a3. Resume at step 7

6b. Customer chooses to save payment method for future use:
    6b1. System securely stores payment token
    6b2. Resume at step 7

*a. At any time, customer abandons checkout:
    *a1. System preserves cart contents for 30 days
    *a2. Use case ends in failure

7a. Inventory no longer available for one or more items:
    7a1. System identifies affected items
    7a2. Customer removes items or selects alternatives
    7a3. Resume at step 2
-->

**Xa. [Condition]:**
  - Xa1. [Step]
  - Xa2. [Step]
  - Xa3. Resume at step X / Use case ends

**Xb. [Condition]:**
  - Xb1. [Step]
  - Xb2. Use case ends

## Special Requirements

<!--
Non-functional requirements specific to THIS use case (not system-wide).
System-wide NFRs belong in Supplementary Specifications.

Examples:
- Checkout must complete within 30 seconds under normal load
- Payment page must be PCI-DSS compliant
- Order confirmation must be accessible (WCAG 2.1 AA)
-->

## Open Issues

<!--
Unresolved questions that need stakeholder input.

Examples:
- Should guests be able to checkout, or require account creation?
- What's the policy for partial shipments if some items are backordered?
- How long should abandoned carts be preserved?
-->
