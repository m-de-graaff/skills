# Release Verdicts

- `BLOCK RELEASE`: the change is unsafe to ship.
- `RELEASE WITH FIXES`: the change can ship after specific fixes are applied.
- `SAFE TO DEPLOY`: the change is ready and low risk.
- `SAFE TO DEPLOY WITH MONITORING`: the change is ready, but needs watchpoints or alerting.

## Checklist

- Migration path and rollback are clear.
- Deploy path is known and reproducible.
- Environment variables are present in every target environment.
- Smoke test or preview coverage exists for the risky path.
- Rollout has an owner and a fallback.
