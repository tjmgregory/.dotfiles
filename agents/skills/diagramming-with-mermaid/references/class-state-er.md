# Class, State, and ER Diagram Reference

## Contents
- [Class Diagram](#class-diagram)
- [State Diagram](#state-diagram)
- [Entity Relationship Diagram](#entity-relationship-diagram)

---

# Class Diagram

## Declaration

```
classDiagram
```

## Class Definition

```
class Animal {
    +String name
    +int age
    #List~String~ tags
    -UUID id
    +getName() String
    +setName(String name) void
    #validate()* void
    +getInstance()$ Animal
}
```

**Visibility:** `+` Public, `-` Private, `#` Protected, `~` Package/Internal

**Method classifiers** (after return type): `*` Abstract, `$` Static

**Generics**: Use tildes: `List~String~`, `Map~String, List~int~~`

## Annotations

```
class Shape {
    <<interface>>
}
class Color {
    <<enumeration>>
    RED
    GREEN
    BLUE
}
```

Types: `<<interface>>`, `<<abstract>>`, `<<service>>`, `<<enumeration>>`

## Class Labels

```
class BankAccount["Bank Account with spaces"]
```

## Relationships

| Type | Syntax | Description |
|------|--------|-------------|
| Inheritance | `A <\|-- B` | B extends A |
| Composition | `A *-- B` | B is part of A (strong) |
| Aggregation | `A o-- B` | B belongs to A (weak) |
| Association | `A --> B` | A uses B |
| Solid link | `A -- B` | Related |
| Dependency | `A ..> B` | A depends on B |
| Realization | `A ..\|> B` | B implements A |
| Dashed link | `A .. B` | Loosely related |

**Bidirectional**: `A <\|..\|> B`

**Lollipop interfaces**: `A ()-- B` or `B --() A`

**Labels**: `A --> B : uses`

**Cardinality**: `A "1" --> "*" B : has`, `A "0..1" --> "1..*" B`

## Namespaces

```
namespace Payments {
    class PaymentProcessor
    class Invoice
}
```

## Notes

```
note "General note"
note for ClassName "Specific note"
```

## Direction

`direction TB`, `BT`, `LR`, `RL`

## Styling

```
classDef highlight fill:#f96,stroke:#333,stroke-width:2px
class Animal highlight
Animal:::highlight
```

Config: `hideEmptyMembersBox: true`

## Example

```mermaid
classDiagram
    direction TB
    namespace Domain {
        class Order {
            <<aggregate root>>
            -UUID id
            -OrderStatus status
            -List~OrderLine~ lines
            -Money total
            +addLine(Product p, int qty) void
            +submit()* void
            +cancel() void
        }
        class OrderLine {
            -UUID id
            -Product product
            -int quantity
            -Money subtotal
        }
        class OrderStatus {
            <<enumeration>>
            DRAFT
            SUBMITTED
            CONFIRMED
            SHIPPED
            CANCELLED
        }
    }
    namespace Services {
        class OrderService {
            <<service>>
            +createOrder(Customer c) Order
            +submitOrder(UUID orderId) void
        }
        class PaymentGateway {
            <<interface>>
            +charge(Money amount)* boolean
            +refund(UUID txnId)* boolean
        }
    }

    Order *-- OrderLine : contains
    Order --> OrderStatus : has
    OrderService --> Order : manages
    OrderService ..> PaymentGateway : uses
```

---

# State Diagram

## Declaration

```
stateDiagram-v2
```

Use `stateDiagram-v2` (preferred over legacy `stateDiagram`).

## States

```
StateId
state "Long description" as StateId
StateId : Description added after
```

## Start and End

```
[*] --> FirstState
LastState --> [*]
```

`[*]` is start or end depending on arrow direction.

## Transitions

```
State1 --> State2
State1 --> State2 : trigger / action
```

## Composite (Nested) States

```
state Active {
    [*] --> Processing
    Processing --> Validating
    Validating --> [*]
}
```

Multiple nesting levels supported.

## Choice

```
state check <<choice>>
[*] --> check
check --> Approved : amount < 1000
check --> NeedsReview : amount >= 1000
```

## Fork and Join

```
state fork_state <<fork>>
state join_state <<join>>
[*] --> fork_state
fork_state --> TaskA
fork_state --> TaskB
TaskA --> join_state
TaskB --> join_state
join_state --> Done
```

## Concurrency

```
state Parallel {
    [*] --> DownloadingData
    --
    [*] --> RenderingUI
}
```

`--` separator creates concurrent regions.

## Notes

```
note right of Active
    This is a note about
    the Active state
end note
note left of Idle : Short note
```

## Direction

`direction LR`, `TB`, `BT`, `RL`. Can be set globally or per composite state.

## Styling

```
classDef alert fill:#f00,color:#fff,font-weight:bold
class Error alert
```

**Limitations**: Cannot style `[*]` start/end or composite states directly.

## Example

```mermaid
stateDiagram-v2
    direction LR
    [*] --> Idle

    state "Order Processing" as Processing {
        direction TB
        [*] --> Validating
        state validation_check <<choice>>
        Validating --> validation_check
        validation_check --> PaymentPending : valid
        validation_check --> Rejected : invalid

        state PaymentPending {
            [*] --> ChargingCard
            ChargingCard --> PaymentConfirmed
            ChargingCard --> PaymentFailed
        }
    }

    Idle --> Processing : order submitted
    Processing --> Fulfillment : payment confirmed
    Processing --> Idle : rejected/failed

    state Fulfillment {
        state fork_ship <<fork>>
        state join_ship <<join>>
        [*] --> fork_ship
        fork_ship --> Picking
        fork_ship --> LabelPrinting
        Picking --> join_ship
        LabelPrinting --> join_ship
        join_ship --> Shipped
    }

    Fulfillment --> Delivered
    Delivered --> [*]
```

---

# Entity Relationship Diagram

## Declaration

```
erDiagram
```

## Relationship Syntax

```
ENTITY1 ||--o{ ENTITY2 : "relationship label"
```

Format: `ENTITY1 [cardinality][line][cardinality] ENTITY2 : label`

## Cardinality Markers

| Left | Right | Meaning |
|------|-------|---------|
| `\|o` | `o\|` | Zero or one |
| `\|\|` | `\|\|` | Exactly one |
| `}o` | `o{` | Zero or more |
| `}\|` | `\|{` | One or more |

## Line Types

- `--` Solid (identifying relationship: child depends on parent)
- `..` Dashed (non-identifying: entities exist independently)

## Entity Attributes

```
CUSTOMER {
    int id PK
    string name
    string email UK
    int address_id FK
    string phone PK,FK "customer primary phone"
}
```

Format: `type name [keys] ["comment"]`. Keys: `PK`, `FK`, `UK`. Combine: `PK,FK`.

## Entity Aliases

```
CUSTOMER ["Customer Account"] {
    ...
}
```

## Direction

```
erDiagram
    direction LR
```

## Styling

```
classDef highlight fill:#f9f,stroke:#333
CUSTOMER:::highlight
style CUSTOMER fill:#bbf,stroke:#333
```

## Example

```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    CUSTOMER {
        int id PK
        string first_name
        string last_name
        string email UK
        date created_at
    }

    ORDER ||--|{ ORDER_LINE : contains
    ORDER {
        int id PK
        int customer_id FK
        date order_date
        string status
        decimal total
    }

    ORDER_LINE }o--|| PRODUCT : references
    ORDER_LINE {
        int id PK
        int order_id FK
        int product_id FK
        int quantity
        decimal unit_price
    }

    PRODUCT ||--o{ PRODUCT_CATEGORY : "categorized by"
    PRODUCT {
        int id PK
        string name
        string sku UK
        decimal price
        int stock_qty
    }

    CATEGORY ||--o{ PRODUCT_CATEGORY : groups
    CATEGORY {
        int id PK
        string name
        int parent_id FK "self-referencing"
    }

    PRODUCT_CATEGORY {
        int product_id PK,FK
        int category_id PK,FK
    }
```
