# Remediation Playbooks

## Deletion First

Before extracting anything, look for:

- Dead code
- Unused exports
- Stale feature flags
- Deprecated branches
- Duplicate types
- Redundant wrappers
- Compatibility paths that no longer need to exist

## Preferred Extraction Order

1. Delete dead code.
2. Delete thin wrappers.
3. Collapse fake layers.
4. Extract real boundaries.
5. Delete temporary bridges after callers migrate.

## Playbook - 1,000+ LOC File

1. Identify the file's responsibilities.
2. Mark generated or vendor exceptions if applicable.
3. Delete dead code first.
4. Extract pure functions with tests.
5. Extract IO boundaries.
6. Extract use cases or subcomponents.
7. Keep a temporary facade only if callers require migration.
8. Stop new behavior from entering the old file.
9. Delete the facade after callers migrate.

## Playbook - God Service

1. List every use case in the service.
2. Group methods by workflow.
3. Move provider calls to adapters.
4. Move queries to repositories.
5. Move policy rules to domain or policy modules.
6. Create focused use-case modules.
7. Replace the old service with a temporary compatibility facade only if needed.

## Playbook - God Component

1. Separate data loading from rendering.
2. Split filters, forms, dialogs, tables, and charts.
3. Move business rules to server or domain logic.
4. Keep the page as a composition layer.

## Playbook - Duplicate Business Rule

1. Identify the authoritative source of truth.
2. Delete weaker copies.
3. Centralize the rule in the correct layer.
4. Add tests that prove all entry points use the same rule.

## Playbook - Thin Wrapper Chain

1. Draw the call chain.
2. Mark layers that only forward input and output.
3. Delete pass-through layers.
4. Keep one real boundary around external IO or domain policy.
