# Security Policy

## Current Project Status

This repository is currently in its **documentation phase** — no deployed service, API, or production system exists yet (see [`docs/15_ROADMAP.md`](docs/15_ROADMAP.md)). Once the H0 prototype and later phases are implemented, this policy will be updated with concrete scope (deployed endpoints, supported versions, etc.). Until then, "security" primarily concerns the integrity of the documentation and, once code lands, standard application security practice as defined in [`docs/11_SECURITY_ARCHITECTURE.md`](docs/11_SECURITY_ARCHITECTURE.md).

## Reporting a Vulnerability or Security Concern

**Please do not open a public GitHub issue for security vulnerabilities.**

Instead, please report it privately using one of these methods:

1. **Preferred:** Use GitHub's private vulnerability reporting for this repository (**Security → Report a vulnerability** tab), if enabled by the repository maintainers.
2. **Alternative:** Email the maintainers at `<SECURITY_CONTACT_EMAIL — replace before publishing>` with:
   - A description of the concern and its potential impact.
   - Steps to reproduce, if applicable.
   - Any relevant logs, screenshots, or proof-of-concept (kept minimal — do not include real personal data).

We will acknowledge your report within **5 business days** and aim to provide a remediation timeline within **14 business days** of confirmation.

## Scope

**In scope:**
- Vulnerabilities in this repository's own documentation build/lint tooling (e.g., a CI workflow that could be abused to exfiltrate secrets).
- Once implementation begins: vulnerabilities in the API, authentication/authorization (RBAC), data handling, or PII scrubbing pipeline described in `docs/11_SECURITY_ARCHITECTURE.md`.

**Out of scope:**
- Vulnerabilities in Oil India Limited's actual production systems — this project has no relationship to and no access to OIL's real infrastructure (see `NOTICE`). Reports about OIL's real systems should be directed to OIL directly, not to this project.
- Social engineering, physical security, or denial-of-service testing against any deployed demo instance without prior written permission from the maintainers.

## Data Handling Commitments

Per [`docs/01_PROJECT_CONSTITUTION.md`](docs/01_PROJECT_CONSTITUTION.md) and [`docs/11_SECURITY_ARCHITECTURE.md`](docs/11_SECURITY_ARCHITECTURE.md):
- No real OIL operational or confidential data is stored in this repository.
- Any example safety-report text in `/docs` or future `/ml` training fixtures is synthetic/illustrative and must not contain real personally identifiable information (PII).
- If you discover what appears to be real PII or real confidential OIL data anywhere in this repository, please report it using the private channel above — treat it as a security incident, not a routine issue.

## Supported Versions

| Version | Supported |
|---|---|
| `main` (documentation phase) | ✅ |
| Future tagged releases | Will be listed here once they exist |
