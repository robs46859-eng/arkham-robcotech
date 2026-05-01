# Worker Loop Agent Steplist

## Objective
Build and finish the orchestration worker loop in `FullStackArkham` so a vertical workflow can:
1. start in `services/media-commerce`
2. submit into `services/orchestration`
3. dequeue and execute steps
4. checkpoint outputs
5. advance to the next step
6. complete the workflow

## Current State
- `media-commerce` has a workflow submission endpoint:
  - `POST /api/v1/content/strategy/workflow`
  - file: `services/media-commerce/app/main.py`
- orchestration has a registered flow:
  - `media_content_strategy`
  - file: `services/orchestration/app/flows/registry.py`
- orchestration startup now initializes:
  - `CheckpointStore.initialize()`
  - `TaskQueue.initialize()`
  - file: `services/orchestration/app/main.py`
- local import fallbacks already exist in orchestration for:
  - `asyncpg`
  - `redis`
  - `orjson`
  - files:
    - `services/orchestration/app/checkpoints.py`
    - `services/orchestration/app/queues.py`
- tests currently passing for:
  - `services/media-commerce/tests/*`
  - `services/orchestration/tests/test_media_content_strategy_flow.py`

## Important Constraints
- Keep the horizontal core in orchestration, not in `media-commerce`.
- Do not move workflow state logic into the vertical service.
- Avoid introducing real network dependencies in tests.
- Use deterministic behavior where possible.
- Respect the existing `app` package-name collision between `services/media-commerce/app` and `services/orchestration/app`; test imports must isolate module context.

## Files Already Touched
- `services/media-commerce/app/main.py`
- `services/media-commerce/app/settings.py`
- `services/orchestration/app/main.py`
- `services/orchestration/app/flows/registry.py`
- `services/orchestration/app/checkpoints.py`
- `services/orchestration/app/queues.py`
- `services/orchestration/tests/test_media_content_strategy_flow.py`
- `services/media-commerce/tests/test_content_strategy_workflow_submission.py`

## Remaining Work

### 1. Add a real worker-loop module
Create something like:
- `services/orchestration/app/worker.py`

It should provide:
- `WorkflowWorker`
- `process_next_task()`
- `drain(max_tasks=...)`
- optional `run_forever(poll_interval=...)`

Expected behavior:
- dequeue one task from `workflow_tasks`
- load workflow from `CheckpointStore`
- skip cancelled/completed workflows
- resolve executor from `TaskExecutorRegistry`
- execute task
- write step output into `workflow["workflow_state"][step_name]`
- checkpoint successful step output
- enqueue next step if one exists
- mark workflow completed when final step finishes
- mark workflow failed and store `last_checkpoint` when a step fails

### 2. Register the media-commerce executor
Add a new executor registration in:
- `services/orchestration/app/tasks/__init__.py`

There is already a candidate file created:
- `services/orchestration/app/tasks/media_content.py`

Make sure it is imported and registered via:
- `ContentStrategyGenerationExecutor`

### 3. Switch the `media_content_strategy` flow to use the new executor
In `services/orchestration/app/flows/registry.py`:
- use `content_strategy_generation` as the core step
- avoid fragile previous-step guessing by setting explicit config like:
  - `input_step`
  - `input_field`

Recommended step sequence:
1. `generate_content_strategy`
2. `validate_content_strategy`
3. `store_content_strategy_artifact`

### 4. Harden executor input chaining
Current executors like:
- `SchemaValidationExecutor`
- `ArtifactStorageExecutor`
- `PolicyEvaluationExecutor`

still rely on `_get_previous_step_name()` heuristics.

Add support for explicit config:
- `input_step`
- `input_field`

Behavior:
- if `input_step` is present, use that workflow-state entry directly
- otherwise preserve existing fallback behavior

### 5. Expose worker controls for local verification
Add bounded endpoints in orchestration, for example:
- `POST /api/v1/worker/run-once`
- `POST /api/v1/worker/drain`

These should call the worker-loop methods on `app.state.worker`.

Do not build an unbounded background daemon first. Start with deterministic callable entrypoints.

### 6. Initialize worker runtime on startup
In `services/orchestration/app/main.py`, initialize:
- `app.state.executor_registry`
- `app.state.worker`

Use:
- `create_executor_registry()`
- `WorkflowWorker(...)`

### 7. Add tests for the worker loop
Add tests under:
- `services/orchestration/tests/`

Minimum set:
- worker processes one task and enqueues the next step
- worker completes a full `media_content_strategy` workflow
- worker marks workflow failed on executor failure
- worker endpoints `run-once` / `drain` return deterministic status payloads

### 8. Re-run verification
Run at minimum:
```bash
python3 -m pytest services/orchestration/tests
python3 -m pytest services/media-commerce/tests services/orchestration/tests
```

### 9. Refresh graph
After code changes:
```bash
cd /Users/joeiton/Desktop/FullStackArkham
graphify update .
```

## Notes for the Next Agent
- The last meaningful progress was wiring the vertical submission endpoint and the registered flow.
- The missing piece is the actual task execution loop and explicit chaining between steps.
- The most likely failure mode is Python import collision between the two `app.*` packages. Clear `sys.modules["app"...]` in tests when switching service contexts.
