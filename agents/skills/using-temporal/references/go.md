# Temporal Go SDK

## Installation

```bash
go get go.temporal.io/sdk
```

## Basic Structure

```go
// workflows/order.go
package workflows

import (
    "time"
    "go.temporal.io/sdk/workflow"
    "go.temporal.io/sdk/activity"
    "myapp/activities"
)

func OrderWorkflow(ctx workflow.Context, orderID string) (string, error) {
    ao := workflow.ActivityOptions{
        StartToCloseTimeout: 30 * time.Second,
        RetryPolicy: &temporal.RetryPolicy{
            MaximumAttempts: 3,
        },
    }
    ctx = workflow.WithActivityOptions(ctx, ao)

    if err := workflow.ExecuteActivity(ctx, activities.ChargeCard, orderID).Get(ctx, nil); err != nil {
        return "", err
    }

    if err := workflow.Sleep(ctx, 24*time.Hour); err != nil {
        return "", err
    }

    if err := workflow.ExecuteActivity(ctx, activities.SendEmail, orderID, "shipped").Get(ctx, nil); err != nil {
        return "", err
    }
    return "completed", nil
}

// activities/activities.go
package activities

import "context"

func ChargeCard(ctx context.Context, orderID string) error {
    return stripe.Charge(orderID)
}

func SendEmail(ctx context.Context, orderID, status string) error {
    return mailer.Send(orderID, status)
}

// worker/main.go
package main

import (
    "go.temporal.io/sdk/client"
    "go.temporal.io/sdk/worker"
    "myapp/workflows"
    "myapp/activities"
)

func main() {
    c, _ := client.Dial(client.Options{})
    defer c.Close()

    w := worker.New(c, "my-queue", worker.Options{})
    w.RegisterWorkflow(workflows.OrderWorkflow)
    w.RegisterActivity(activities.ChargeCard)
    w.RegisterActivity(activities.SendEmail)
    w.Run(worker.InterruptCh())
}
```

## Signals & Queries

```go
func OrderWorkflow(ctx workflow.Context, orderID string) (string, error) {
    cancelCh := workflow.GetSignalChannel(ctx, "cancel")
    status := "processing"

    workflow.SetQueryHandler(ctx, "getStatus", func() (string, error) {
        return status, nil
    })

    // Wait for signal or timeout
    selector := workflow.NewSelector(ctx)
    selector.AddReceive(cancelCh, func(c workflow.ReceiveChannel, more bool) {
        status = "cancelled"
    })

    timerFuture := workflow.NewTimer(ctx, 30*24*time.Hour)
    selector.AddFuture(timerFuture, func(f workflow.Future) {
        status = "completed"
    })

    selector.Select(ctx)
    return status, nil
}
```

## Versioning

```go
func OrderWorkflow(ctx workflow.Context, orderID string) error {
    v := workflow.GetVersion(ctx, "added-email-step", workflow.DefaultVersion, 1)
    if v == 1 {
        // New code path
        workflow.ExecuteActivity(ctx, SendWelcomeEmail, orderID).Get(ctx, nil)
    }
    // rest of workflow
    return nil
}
```

## Testing

```go
func TestOrderWorkflow(t *testing.T) {
    testSuite := &testsuite.WorkflowTestSuite{}
    env := testSuite.NewTestWorkflowEnvironment()

    env.RegisterActivity(activities.ChargeCard)
    env.RegisterActivity(activities.SendEmail)

    // Mock activity
    env.OnActivity(activities.ChargeCard, mock.Anything, "order-1").Return(nil)
    env.OnActivity(activities.SendEmail, mock.Anything, "order-1", "shipped").Return(nil)

    env.ExecuteWorkflow(workflows.OrderWorkflow, "order-1")

    require.True(t, env.IsWorkflowCompleted())
    require.NoError(t, env.GetWorkflowError())
    var result string
    env.GetWorkflowResult(&result)
    assert.Equal(t, "completed", result)
}
```

## Common Gotchas

- **Determinism**: Use `workflow.Now(ctx)` not `time.Now()`. Use `workflow.GetLogger(ctx)` not `log`.
- **Activity registration**: Activities can be registered as functions or as methods on a struct (useful for injecting dependencies).
- **Context cancellation**: Temporal uses its own `workflow.Context` — don't mix with standard `context.Context` in workflow code.
- **Goroutines**: Use `workflow.Go()` instead of `go` for coroutines inside workflows.
- **Panic handling**: Panics in activities are caught and converted to errors; panics in workflows cause the worker to crash.
