# Temporal Cross-Language Patterns

## Table of Contents
- [Signals & Queries](#signals--queries)
- [Child Workflows](#child-workflows)
- [Schedules](#schedules)
- [Error Handling](#error-handling)
- [Versioning](#versioning)
- [Saga Pattern (Compensation)](#saga-pattern-compensation)
- [Fan-out / Parallel Activities](#fan-out--parallel-activities)
- [Continue-as-New](#continue-as-new)
- [Heartbeating Long Activities](#heartbeating-long-activities)
- [Deployment Patterns](#deployment-patterns)

---

## Signals & Queries

**Signals** — async, fire-and-forget messages sent into a running workflow. The workflow handles them at a convenient point.

**Queries** — synchronous reads of workflow state; never modify state.

**Updates** (Temporal ≥1.21) — like signals but return a value and can be validated/rejected before applying.

Use signals for: pause/resume, cancel, inject new data.
Use queries for: status checks, progress reporting.
Use updates for: request-response interactions with a running workflow.

---

## Child Workflows

Use child workflows to:
- Break large workflows into manageable units
- Apply different retry/timeout policies to subsections
- Run independent parallel branches

```
Parent Workflow
├── Child A (runs in parallel)
├── Child B (runs in parallel)
└── waits for both
```

Child workflows run on the same or different task queue. They have their own history and can be cancelled independently.

---

## Schedules

Schedules replace the old cron workflow pattern. Prefer schedules over embedding `cronSchedule` in workflow options.

Key features:
- Pause/resume/trigger manually via CLI or SDK
- Backfill missed runs
- `overlapPolicy`: skip, buffer, cancel previous, or allow all
- `catchupWindow`: how far back to backfill on startup

```bash
# CLI management
temporal schedule create --schedule-id my-sched --cron "0 9 * * MON-FRI" \
  --workflow-type MyWorkflow --task-queue my-queue

temporal schedule pause --schedule-id my-sched
temporal schedule trigger --schedule-id my-sched  # immediate run
temporal schedule delete --schedule-id my-sched
```

---

## Error Handling

**Activity failures**: Temporal wraps them in `ActivityFailure`. The inner error is the original.

**Application failures**: Use these for business logic errors. Mark non-retryable when retrying won't help (e.g., invalid input, missing resource).

**Workflow failures**: If a workflow returns an error/exception, it's marked as failed. Temporal doesn't auto-retry failed workflows (unlike activities).

**Cancel requests**: Workflows receive cancellation as a special signal. Handle `CanceledError` / `workflow.Canceled` to do cleanup.

Strategy:
1. Mark truly unrecoverable errors as non-retryable immediately
2. Set `scheduleToCloseTimeout` to bound total retry duration
3. Use compensation (saga) for multi-step rollback

---

## Versioning

When you change workflow logic, in-flight workflows replay their history against the new code. If the history diverges from the new code path → non-determinism error → workflow stuck.

**The rule**: Any change to the execution path of a workflow requires versioning.

Safe changes (no versioning needed):
- Adding/changing activity implementations (activities aren't replayed)
- Changing retry policies
- Adding new workflows
- Changing activity input/output types (if backward compatible)

Unsafe changes (require versioning):
- Adding/removing/reordering activity calls
- Adding/removing `sleep()` calls
- Changing workflow function signature
- Adding/removing signal/query handlers

**Patching workflow**:
1. Add `patched("change-id")` check
2. Deploy new worker
3. Wait for all pre-patch workflows to complete
4. Replace with `deprecatePatch("change-id")`
5. Deploy again
6. Eventually remove the patch entirely

---

## Saga Pattern (Compensation)

For distributed transactions where you need rollback:

```
OrderWorkflow:
  1. reserveInventory()     → on failure: releaseInventory()
  2. chargePayment()        → on failure: refundPayment()
  3. scheduleShipment()     → on failure: cancelShipment()
```

```typescript
// TypeScript example
const compensations: Array<() => Promise<void>> = [];

try {
  await reserveInventory(orderId);
  compensations.push(() => releaseInventory(orderId));

  await chargePayment(orderId);
  compensations.push(() => refundPayment(orderId));

  await scheduleShipment(orderId);
} catch (err) {
  // Run compensations in reverse
  for (const comp of compensations.reverse()) {
    await comp(); // each is its own retried activity
  }
  throw err;
}
```

---

## Fan-out / Parallel Activities

```typescript
// TypeScript — run activities in parallel
const results = await Promise.all(
  items.map(item => chargeItem(item))
);

// With partial failure handling
const results = await Promise.allSettled(
  items.map(item => chargeItem(item))
);
```

```python
# Python — parallel activities
handles = [
    workflow.execute_activity(process_item, item, start_to_close_timeout=timedelta(seconds=30))
    for item in items
]
results = await asyncio.gather(*handles)
```

For large fan-outs (thousands of items), use child workflows to avoid giant histories. Each child workflow has its own history.

---

## Continue-as-New

Workflows have a history size limit (~50k events, ~50MB). Long-running workflows (e.g., cron-style loops, perpetual processes) must use `continueAsNew` to reset history while preserving state.

```typescript
import { continueAsNew, isCancellation } from '@temporalio/workflow';

export async function perpetualWorkflow(state: MyState): Promise<void> {
  // do work...
  await processNextBatch(state);

  // Reset history, passing updated state to fresh execution
  await continueAsNew<typeof perpetualWorkflow>({ ...state, iteration: state.iteration + 1 });
}
```

Rule of thumb: call `continueAsNew` every ~1000–5000 iterations, or when history approaches 10k events.

---

## Heartbeating Long Activities

Activities that run for minutes/hours must heartbeat to prove they're still alive. If the worker dies, Temporal detects the missed heartbeat and reschedules the activity.

```typescript
import { activityInfo, heartbeat, isCancellation, sleep } from '@temporalio/activity';

export async function longRunningActivity(input: Input): Promise<Output> {
  const { heartbeatDetails } = activityInfo();
  let progress = heartbeatDetails ?? 0; // resume from last checkpoint

  while (progress < 100) {
    await doWork(progress);
    progress++;
    heartbeat(progress); // report checkpoint

    // Check for cancellation
    try {
      await sleep(100); // brief pause
    } catch (err) {
      if (isCancellation(err)) throw err; // propagate cancel
    }
  }
  return result;
}
```

Set `heartbeatTimeout` in activity options (e.g., `30s`). Temporal reschedules if no heartbeat within that window.

---

## Deployment Patterns

**Blue/green worker deploys**: Deploy new workers alongside old ones. Both poll the same task queue. Old workers finish in-flight tasks; new workers pick up new ones. Once old workers drain, shut them down.

**Namespace isolation**: Use separate namespaces for prod/staging/dev. Namespaces are completely isolated (separate history, workers, task queues).

**Task queue per service tier**: 
- `orders-critical` → high-priority workers (more instances)
- `orders-batch` → low-priority workers (fewer instances, cheaper infra)

**Worker versioning** (Temporal ≥1.21 / Cloud): Assign build IDs to workers and task queues to route workflows to compatible worker versions. Replaces the patching workflow for major version migrations.
