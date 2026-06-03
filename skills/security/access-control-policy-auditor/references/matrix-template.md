# Access Control Matrix Template

Use this as the default review artifact.

| Actor | Resource | Action | Allowed? | Enforced where? | Test exists? |
|---|---|---|---|---|---|
| User | Own account | Read | Yes | Policy layer | Yes |
| Member | Other org's resource | Read | No | RLS and service policy | Yes |

## Notes

- Prefer the authoritative policy layer over UI-only checks.
- Flag any admin or support bypass explicitly.
- For Supabase-heavy apps, check that RLS and application policy agree.
- For billing-plan permissions, verify plan changes and membership changes stay synchronized.
