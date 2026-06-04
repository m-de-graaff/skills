---
name: cookie-consent-review
description: Review cookies and tracking: CMPs, pixels, analytics, ads, SDKs, opt-outs, consent, disclosures.
---

# Cookie Consent Review

Map tracking technologies, classify them, check whether consent or opt-out may be required, and produce implementation issues. This is not legal advice; verify current regional cookie, tracking, and opt-out rules from official sources or user-provided legal materials.

## Workflow

1. Inventory cookies, pixels, scripts, SDKs, server-side events, consent-mode calls, and tracking requests.
2. Classify each technology by purpose and necessity.
3. Identify personal data, identifiers, vendors, onward sharing, and region behavior.
4. Check consent, opt-out, preference-state handling, and whether tags fire before consent.
5. Check disclosures, withdrawal path, and preference center behavior.
6. Produce remediation issues.

## Classification Table

```text
Technology | Vendor | Purpose | Data/identifier | Category | Fires before consent? | Consent/opt-out state | Region behavior | Risk
```

Categories:

- Strictly necessary
- Preferences
- Analytics
- Advertising/marketing
- Personalisation
- Security/fraud
- Unknown

## Red Flags

- Ads or analytics tags firing before consent where consent is required.
- Consent state not propagated to tags.
- No withdrawal path.
- Dark-pattern banner or reject path harder than accept path.
- Vendor claims not verified.
- Server-side tracking bypasses frontend consent.
- Session replay captures personal data.
- Sensitive pages tracked by marketing pixels.
- GPC or opt-out preference signals ignored where applicable.

## Output

- Tracking inventory
- Consent/opt-out gaps
- Disclosure gaps
- Vendor risks
- Engineering remediation issues
