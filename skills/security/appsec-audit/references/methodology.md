# Methodology

Use these defensive AppSec references for structure and terminology:

- OWASP Web Security Testing Guide: https://owasp.org/www-project-web-security-testing-guide/
- OWASP Application Security Verification Standard: https://owasp.org/www-project-application-security-verification-standard/
- MITRE CWE: https://cwe.mitre.org/
- FIRST CVSS v4.0: https://www.first.org/cvss/v4-0

## How To Use These References

- Use OWASP WSTG for web testing structure and categories.
- Use OWASP ASVS for control-oriented verification and acceptance criteria.
- Use CWE for weakness classification when writing formal reports.
- Use CVSS v4.0 only when the user asks for formal scoring or the report needs a security-program-compatible score.

## Alignment Rules

- Prefer source-aware and architecture-aware review over generic scanner output.
- Use standards mappings to clarify, not to pad the report.
- Do not cite a standard as proof that a finding is exploitable.
- Confirm reachability and impact before assigning high severity.
- Where evidence is limited, mark the finding as Probable or Needs validation.
