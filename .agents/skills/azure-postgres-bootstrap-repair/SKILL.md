---
name: azure-postgres-bootstrap-repair
description: Use when FullStackArkham PostgreSQL initialization fails during Azure deploy because of extension allowlists, schema or seed mismatches, non-idempotent SQL, typed NULL issues, or partial bootstrap replay problems, and an agent needs to repair the SQL and resume path safely.
---

# Azure Postgres Bootstrap Repair

Use this skill when database initialization fails in `scripts/deploy-bot.sh` or when `infra/docker/postgres/*.sql` drifts from the live schema assumptions.

Primary files:
- `scripts/deploy-bot.sh`
- `infra/docker/postgres/init.sql`
- `infra/docker/postgres/init-resume.sql`
- `infra/docker/postgres/init-verticals.sql`
- `infra/docker/postgres/init-verticals-resume.sql`

## Workflow

1. Identify the failing SQL file and exact statement.
Common sources:
- `init.sql`
- `init-resume.sql`
- `init-verticals.sql`
- `init-verticals-resume.sql`

2. Compare the failing insert or DDL against the table definition in the same file.
Look for:
- insert references a missing column
- seed expects nullable data but the column is `NOT NULL`
- comments contradict actual schema
- a table or constraint name changed without seed updates

3. Check Azure-only prerequisites before changing schema logic.
For this repo, extension allowlisting is mandatory before `CREATE EXTENSION`:
- `uuid-ossp`
- `pg_trgm`
- `vector`

The deploy script should set `azure.extensions` before replaying SQL.

4. Repair for idempotency, not just the current run.
Prefer:
- `CREATE TABLE IF NOT EXISTS`
- `ALTER TABLE ... ADD COLUMN IF NOT EXISTS`
- explicit existence checks for seeds
- resume SQL files for partial first-run recovery

Do not rely on `ON CONFLICT DO NOTHING` unless a real unique or primary-key conflict target can fire for the intended duplicate case.

5. Treat partial bootstrap as normal after first failure.
Add or update sentinel checks in `scripts/deploy-bot.sh` so retries:
- skip already-complete phases
- resume the remaining SQL
- avoid dropping the database unless explicitly requested

6. Watch type inference in `VALUES`.
If a seed row uses `NULL` for typed columns like `uuid`, cast it explicitly:
- `NULL::uuid`
- `NULL::varchar(50)`

Without casts, `VALUES` may infer `text` and break comparisons in idempotency checks.

7. Keep global vs tenant-scoped data explicit.
If a table supports global rows, the schema must permit them.
If the schema requires tenant ownership, seed rows must use a real tenant id.
Do not leave those semantics ambiguous in comments.

## Repair Patterns

### Missing-column seed mismatch
- Fix the insert to match the actual table columns.
- Then inspect nearby seeds for the same outdated assumption.

### Nullable global policy mismatch
- If comments and behavior require global rows, drop `NOT NULL`.
- If tenant scope is actually required, replace `NULL` seeds with a real tenant id.

### Non-idempotent seed
- Replace unconditional insert or weak `ON CONFLICT DO NOTHING` with:
  `INSERT ... SELECT ... WHERE NOT EXISTS (...)`
- Match on the natural uniqueness actually intended by the seed.

### Partial bootstrap replay
- Add a `*-resume.sql` file when replaying the original file would fail on existing objects.
- Gate the resume path in `scripts/deploy-bot.sh` with sentinel table checks.

## Validation

After repairs:
- `bash -n scripts/deploy-bot.sh`
- inspect the changed SQL around the failing statement
- rerun the deploy only after the resume path is in place

If the next failure moves forward into a new statement, continue from the new blocker instead of resetting the database.

## References

Read when needed:
- `references/architecture.md`
- `references/graphify.md`
