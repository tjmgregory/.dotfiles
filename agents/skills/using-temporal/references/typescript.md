# Temporal TypeScript SDK

## Installation

```bash
npm install @temporalio/client @temporalio/worker @temporalio/workflow @temporalio/activity
```

## Project Structure

```
src/
├── workflows.ts      # Workflow definitions (bundled by Temporal, runs in isolate)
├── activities.ts     # Activity implementations (runs in Node.js process)
├── worker.ts         # Worker setup
└── client.ts         # Client for starting/signaling workflows
```

**Important**: Workflow code is bundled into a V8 isolate — it cannot import Node.js built-ins or most npm packages directly. Use `proxyActivities` for anything that needs I/O.

## Signals & Queries

```typescript
// workflows.ts
import { defineSignal, defineQuery, setHandler, condition } from '@temporalio/workflow';

export const cancelSignal = defineSignal('cancel');
export const getStatusQuery = defineQuery<string>('getStatus');

export async function orderWorkflow(orderId: string): Promise<void> {
  let cancelled = false;
  let status = 'processing';

  setHandler(cancelSignal, () => { cancelled = true; });
  setHandler(getStatusQuery, () => status);

  // Wait for condition or timeout
  const wasCancelled = await condition(() => cancelled, '30 days');

  status = wasCancelled ? 'cancelled' : 'completed';
}

// client.ts — send signal
await client.workflow.getHandle('order-123').signal(cancelSignal);

// client.ts — query
const status = await client.workflow.getHandle('order-123').query(getStatusQuery);
```

## Child Workflows

```typescript
import { startChild, executeChild } from '@temporalio/workflow';

// Fire and forget
const handle = await startChild(subWorkflow, {
  args: [input],
  taskQueue: 'my-queue',
});

// Wait for result
const result = await executeChild(subWorkflow, { args: [input] });
```

## Schedules (Cron)

```typescript
// client.ts
await client.schedule.create({
  scheduleId: 'daily-report',
  spec: { cronExpressions: ['0 9 * * MON-FRI'] },
  action: {
    type: 'startWorkflow',
    workflowType: generateReport,
    taskQueue: 'reports',
  },
});
```

## Updates (Temporal ≥1.21)

Updates are like signals but return a value and can be validated:

```typescript
import { defineUpdate, setHandler } from '@temporalio/workflow';

export const addItemUpdate = defineUpdate<string, [string]>('addItem');

setHandler(
  addItemUpdate,
  (item: string) => {
    items.push(item);
    return `Added ${item}`;
  },
  { validator: (item: string) => { if (!item) throw new Error('Empty item'); } }
);
```

## Versioning (Patching)

```typescript
import { patched } from '@temporalio/workflow';

export async function myWorkflow(): Promise<void> {
  if (patched('added-email-step')) {
    // New code path for new + updated workflows
    await sendWelcomeEmail();
  }
  // Old code path still runs for in-flight workflows that haven't reached this point
}
```

After all pre-patch workflows complete, replace with `deprecatePatch('added-email-step')`, then eventually remove the patch entirely.

## Testing

```typescript
import { TestWorkflowEnvironment } from '@temporalio/testing';
import { Worker } from '@temporalio/worker';

let env: TestWorkflowEnvironment;

beforeAll(async () => {
  env = await TestWorkflowEnvironment.createLocal();
});
afterAll(() => env.teardown());

it('completes order workflow', async () => {
  const { client, nativeConnection } = env;
  const worker = await Worker.create({
    connection: nativeConnection,
    taskQueue: 'test',
    workflowsPath: require.resolve('./workflows'),
    activities: { chargeCard: async () => {}, sendEmail: async () => {} },
  });

  const result = await worker.runUntil(
    client.workflow.execute(orderWorkflow, {
      taskQueue: 'test',
      workflowId: 'test-order',
      args: ['order-1'],
    })
  );
  expect(result).toBe('completed');
});
```

## Common Gotchas

- **Workflow imports**: Only import from `@temporalio/workflow` in workflow files — not from `@temporalio/client` or `@temporalio/activity`. The bundler will error if you do.
- **Date/time**: Use `workflow.now()` for current time in workflows, not `Date.now()`.
- **Long workflow IDs**: Max 255 characters.
- **Payload size**: Default max payload is 2MB per activity/signal argument. Use a reference pattern (pass IDs, fetch data in activity) for large data.
- **sinon/jest mocks in tests**: Mock at the activity level, not inside workflows.
