# Architecture Patterns

Use this reference to choose target structure and names.

## Feature / Domain Ownership

Prefer this when the product has clear domains:

```text
src/
  features/
    orders/
      api/
      components/
      hooks/
      model/
      queries/
      schemas/
      services/
      tests/
    billing/
    users/
  shared/
    ui/
    lib/
    config/
```

Rules:

- Feature code may import from `shared`.
- `shared` must not import from feature folders.
- Features should not import deeply from unrelated features unless using a documented public interface.
- Shared modules must be genuinely cross-domain and stable.

## Backend Layer Split

Use this split for API-heavy systems:

```text
route/controller -> validation -> auth/policy -> use case -> repository/provider -> mapper/serializer
```

Example:

```text
orders/
  orders.route.ts
  orders.schema.ts
  orders.policy.ts
  create-order.use-case.ts
  orders.repository.ts
  payments.provider.ts
  orders.presenter.ts
  orders.test.ts
```

Controller/route files should not contain SQL, long business workflows, email templates, or third-party API implementation details.

## Frontend Component Split

For large React/Next.js files, split by role:

```text
OrderDashboardPage.tsx
OrderDashboardHeader.tsx
OrderFilters.tsx
OrderTable.tsx
OrderTableRow.tsx
OrderDetailsDialog.tsx
useOrderDashboardData.ts
useOrderFilters.ts
order-dashboard.types.ts
order-dashboard.helpers.ts
```

Rules:

- Page files compose; they should not contain hundreds of lines of UI internals.
- Components render; they should not perform unrelated business workflows.
- Hooks manage data or state; they should not become god hooks.
- Helpers should be local to the feature unless truly shared.

## Repository / Query Split

For database-heavy code:

```text
users.repository.ts
orders.repository.ts
orders.queries.ts
orders.mappers.ts
orders.types.ts
```

Rules:

- Query modules own SQL/ORM calls.
- Use-case modules decide when queries happen.
- Mapping modules convert database rows to domain/application shapes.
- Do not hide many unrelated queries inside `db.ts` or `database.service.ts`.

## Shared Module Rules

A module can live in `shared`, `common`, or `lib` only if:

- It is used by more than one domain or intentionally platform-level.
- It has a narrow, stable purpose.
- It does not import feature/domain modules.
- Its name describes what it does.
- It has tests if it contains logic.

Avoid:

```text
shared/utils.ts
shared/helpers.ts
shared/common.ts
shared/misc.ts
shared/services.ts
```

Prefer:

```text
shared/date/format-date.ts
shared/http/api-error.ts
shared/result/result.ts
shared/config/env.ts
shared/ui/button.tsx
shared/validation/email.ts
```

## Naming Rules

Names should reveal responsibility.

Prefer:

```text
create-order.use-case.ts
orders.repository.ts
order-status-badge.tsx
can-edit-order.ts
format-currency.ts
parse-webhook-event.ts
subscription-proration.ts
```

Avoid:

```text
utils.ts
helpers.ts
common.ts
manager.ts
processor.ts
handler.ts
service.ts
misc.ts
stuff.ts
new.ts
old.ts
final.ts
```

A generic name is acceptable only at a clear architectural boundary, such as `http/client.ts`, `config/env.ts`, or `ui/button.tsx`.
