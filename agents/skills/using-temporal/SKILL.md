---
name: using-temporal
description: Builds reliable distributed systems using Temporal.io — the workflow orchestration platform. Covers workflows, activities, workers, signals, queries, schedules, and SDK patterns for TypeScript, Python, Go, and Java. Use when the user is building with Temporal, asks about workflow durability, needs to implement retries/timeouts, wants to orchestrate long-running processes, or mentions Temporal workers, activities, or the Temporal CLI.
---

# Using Temporal

## Overview

Temporal is a durable execution platform. Workflows are code that runs as if it never fails — Temporal automatically replays them after crashes, network failures, or restarts. Activities are the side-effectful operations (API calls, DB writes) that workflows orchestrate.

## Core Concepts

| Concept | What it is |
|---|---|
| **Workflow** | Deterministic function that orchestrates activities; survives failures via event sourcing |
| **Activity** | Non-deterministic work (I/O, external calls); retried automatically on failure |
| **Worker** | Process that polls task queues and executes workflows/activities |
| **Task Queue** | Named channel connecting clients to workers |
| **Signal** | Async message sent into a running workflow |
| **Query** | Synchronous read of a workflow's state |
| **Schedule** | Cron-like trigger for workflows |
| **Child Workflow** | Workflow spawned by another workflow |

## Workflow Authoring Rules

Workflows **must be deterministic**. The runtime replays history to reconstruct state, so:

- ✅ Use `workflow.sleep()` / `workflow.now()` — NOT `setTimeout` / `new Date()`
- ✅ Use `workflow.random()` — NOT `Math.random()`
- ✅ Call activities for all I/O
- ❌ No `fetch`, DB calls, file I/O, or non-deterministic logic directly in workflow code
- ❌ No module-level side effects that differ between replays

Violations cause **non-determinism errors** on replay — the hardest Temporal bugs to debug.

## SDK Patterns

For language-specific patterns, examples, and gotchas, see:

- **[references/typescript.md](references/typescript.md)** — TypeScript/Node.js SDK
- **[references/python.md](references/python.md)** — Python SDK
- **[references/go.md](references/go.md)** — Go SDK patterns
- **[references/patterns.md](references/patterns.md)** — Cross-language patterns: signals, queries, child workflows, schedules, error handling

## Quick Start (TypeScript)

```typescript
// worker.ts
import { Worker } from '@temporalio/worker';
import * as activities from './activities';

const worker = await Worker.create({
  workflowsPath: require.resolve('./workflows'),
  activities,
  taskQueue: 'my-queue',
});
await worker.run();

// workflows.ts
import { proxyActivities, sleep } from '@temporalio/workflow';
import type * as activities from './activities';

const { sendEmail, chargeCard } = proxyActivities<typeof activities>({
  startToCloseTimeout: '10s',
  retry: { maximumAttempts: 3 },
});

export async function orderWorkflow(orderId: string): Promise<void> {
  await chargeCard(orderId);
  await sleep('1 day');
  await sendEmail(orderId, 'shipped');
}

// activities.ts
export async function chargeCard(orderId: string): Promise<void> {
  // real I/O here — safe because activities are retried, not replayed
  await stripe.charge(orderId);
}

// client.ts
import { Client } from '@temporalio/client';
const client = new Client();
await client.workflow.start(orderWorkflow, {
  taskQueue: 'my-queue',
  workflowId: `order-${orderId}`,
  args: [orderId],
});
```

## Retry & Timeout Configuration

```typescript
// Activity options — set per-activity or as defaults in proxyActivities
const { myActivity } = proxyActivities<typeof activities>({
  startToCloseTimeout: '30s',      // max time for one attempt
  scheduleToCloseTimeout: '5m',    // max total time including all retries
  retry: {
    initialInterval: '1s',
    backoffCoefficient: 2,
    maximumInterval: '30s',
    maximumAttempts: 5,
    nonRetryableErrorTypes: ['InvalidInputError'],
  },
});
```

## Error Handling

```typescript
import { ApplicationFailure } from '@temporalio/workflow';

// In an activity — non-retryable error
throw ApplicationFailure.nonRetryable('Invalid input', 'InvalidInputError');

// In a workflow — catch activity failures
try {
  await chargeCard(orderId);
} catch (err) {
  if (err instanceof ActivityFailure) {
    // handle
  }
}
```

## Temporal CLI

```bash
# Start local dev server (includes Web UI at localhost:8233)
temporal server start-dev

# Start a workflow
temporal workflow start --type OrderWorkflow --task-queue my-queue --input '"order-123"'

# Inspect running workflow
temporal workflow describe --workflow-id order-123

# Send a signal
temporal workflow signal --workflow-id order-123 --name cancel

# Query workflow state
temporal workflow query --workflow-id order-123 --type getStatus

# List workflows
temporal workflow list
```

## Common Architecture Decisions

**Single vs multiple task queues** — Use separate queues for different worker pools (e.g., CPU-bound vs I/O-bound activities, different scaling needs).

**Workflow ID strategy** — Make IDs business-meaningful and idempotent: `order-{orderId}`, `user-{userId}-onboarding`. Use `workflowIdReusePolicy: REJECT_DUPLICATE` to prevent double-processing.

**Activity granularity** — Each activity should be idempotent. Prefer smaller, focused activities over large ones. Temporal retries the whole activity on failure — make sure retrying is safe.

**Versioning** — When changing workflow logic, use `workflow.patched()` (TS/Java) or `workflow.get_version()` (Python/Go) to handle in-flight workflows safely. See [references/patterns.md](references/patterns.md#versioning).
