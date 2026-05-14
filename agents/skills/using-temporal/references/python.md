# Temporal Python SDK

## Installation

```bash
pip install temporalio
```

## Basic Structure

```python
# workflows.py
from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy
import activities  # imported for type hints only

@workflow.defn
class OrderWorkflow:
    @workflow.run
    async def run(self, order_id: str) -> str:
        # Use workflow.execute_activity — not direct calls
        await workflow.execute_activity(
            activities.charge_card,
            order_id,
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RetryPolicy(maximum_attempts=3),
        )
        await workflow.sleep(timedelta(days=1))
        await workflow.execute_activity(
            activities.send_email,
            args=[order_id, "shipped"],
            start_to_close_timeout=timedelta(seconds=10),
        )
        return "completed"

# activities.py
from temporalio import activity

@activity.defn
async def charge_card(order_id: str) -> None:
    # real I/O here
    await stripe.charge(order_id)

@activity.defn
async def send_email(order_id: str, status: str) -> None:
    await mailer.send(order_id, status)

# worker.py
import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
import workflows, activities

async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="my-queue",
        workflows=[workflows.OrderWorkflow],
        activities=[activities.charge_card, activities.send_email],
    )
    await worker.run()

asyncio.run(main())

# client.py
async def start():
    client = await Client.connect("localhost:7233")
    handle = await client.start_workflow(
        workflows.OrderWorkflow.run,
        "order-123",
        id="order-order-123",
        task_queue="my-queue",
    )
    result = await handle.result()
```

## Signals & Queries

```python
from temporalio import workflow

@workflow.defn
class OrderWorkflow:
    def __init__(self):
        self._cancelled = False
        self._status = "processing"

    @workflow.signal
    async def cancel(self) -> None:
        self._cancelled = True

    @workflow.query
    def get_status(self) -> str:
        return self._status

    @workflow.run
    async def run(self, order_id: str) -> str:
        # Wait until cancelled or timeout
        await workflow.wait_condition(
            lambda: self._cancelled,
            timeout=timedelta(days=30),
        )
        self._status = "cancelled" if self._cancelled else "completed"
        return self._status

# Client usage
handle = client.get_workflow_handle("order-order-123")
await handle.signal(workflows.OrderWorkflow.cancel)
status = await handle.query(workflows.OrderWorkflow.get_status)
```

## Versioning

```python
@workflow.run
async def run(self, order_id: str) -> str:
    # Use get_current_history_length or patching for versioning
    version = workflow.patched("added-email-step")
    if version:
        await workflow.execute_activity(send_welcome_email, order_id, ...)
    # rest of workflow
```

## Testing

```python
import pytest
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

@pytest.mark.asyncio
async def test_order_workflow():
    async with await WorkflowEnvironment.start_local() as env:
        async with Worker(
            env.client,
            task_queue="test",
            workflows=[OrderWorkflow],
            activities=[mock_charge_card, mock_send_email],
        ):
            result = await env.client.execute_workflow(
                OrderWorkflow.run,
                "order-1",
                id="test-order",
                task_queue="test",
            )
            assert result == "completed"
```

## Common Gotchas

- **Determinism**: Don't use `datetime.now()`, `random`, or `asyncio.sleep()` in workflows. Use `workflow.now()`, `workflow.random()`, and `workflow.sleep()`.
- **Imports in workflows**: Don't import modules with side effects at module level in workflow files. Temporal sandboxes workflow execution.
- **Activity context**: Use `activity.info()` inside activities to get metadata (attempt number, workflow ID, etc.).
- **Type hints**: Pass activity functions by reference (not strings) for type safety.
- **Async activities**: Both `async def` and sync activities are supported. Use sync for blocking I/O that can't be made async.
