# Contributing to the OIL Safety Intelligence Platform

Thank you for your interest in contributing. This project is currently in its **documentation-first phase** (see [`docs/15_ROADMAP.md`](docs/15_ROADMAP.md)), so most early contributions will be to the documentation set, with implementation contributions following as the H0 prototype phase begins.

## Before You Start

1. Read [`docs/01_PROJECT_CONSTITUTION.md`](docs/01_PROJECT_CONSTITUTION.md) in full. It is the governing source of truth for this project — every other document and every future line of code must remain consistent with it.
2. Skim [`docs/02_PRODUCT_BLUEPRINT.md`](docs/02_PRODUCT_BLUEPRINT.md) and [`docs/15_ROADMAP.md`](docs/15_ROADMAP.md) to understand current scope and priorities.
3. Check open [Issues](../../issues) and [Pull Requests](../../pulls) to avoid duplicate work.

## Ground Rules (Non-Negotiable)

These rules exist because this is a safety-domain project. Contributions that violate them will be asked to change before merge, regardless of otherwise-good quality:

- **No fabricated data or statistics.** Never present synthetic, illustrative, or assumed data as if it were real Oil India Limited (OIL) operational data. Always label synthetic/prototype data as such — see `01_PROJECT_CONSTITUTION.md` §16 and `05_DATA_STRATEGY_AND_LABELING.md`.
- **No claims of official OIL endorsement, deployment, or IOGP certification.** This is an independent hackathon prototype. See `NOTICE`.
- **SIF Potential ≠ fatality prediction.** Do not introduce language implying the system predicts future accidents or deaths. It assesses SIF-potential *indicators in an existing report*. See `01_PROJECT_CONSTITUTION.md` §9.
- **Human-in-the-loop is not optional.** No contribution may introduce fully autonomous safety decision-making (auto-stopping work, auto-escalating without review, etc.) without an explicit, separately-approved change to the Constitution itself.
- **Tag every non-obvious claim.** Use the project's tagging discipline consistently: `[OFFICIAL REQUIREMENT]`, `[PRODUCT DECISION]` / `[PROPOSED DESIGN]`, `[PROTOTYPE ASSUMPTION]`, `[FUTURE ENHANCEMENT]`, `[ILLUSTRATIVE EXAMPLE]`.

## Documentation Changes

Because the 16 documents in `/docs` cross-reference each other extensively (shared requirement IDs, enums, schema names — see `docs/16_DOCUMENT_CONSISTENCY_AUDIT.md`), please:

1. **If your change conflicts with `01_PROJECT_CONSTITUTION.md`**, propose the Constitution change first, in its own PR, with clear reasoning — don't let downstream documents silently drift from it (this is exactly the class of bug `16_DOCUMENT_CONSISTENCY_AUDIT.md` exists to catch).
2. **If your change introduces or modifies a requirement ID** (`FR-`, `AI-`, `UX-`, `HIL-`, `DATA-`, `SEC-`, `NFR-`, `OBS-`), register/update it in `06_TECHNICAL_REQUIREMENTS.md` in the same PR — that document is the single authoritative ID register.
3. **If your change introduces or modifies an enum, table name, or field name**, grep the whole `/docs` folder for existing usages before renaming anything, and update all occurrences in the same PR:
   ```bash
   grep -rn "YOUR_TERM" docs/
   ```
4. Run a self-check before opening the PR (see the docs-lint CI workflow, which runs automatically, but a local pass catches issues earlier):
   ```bash
   grep -rn "FIXME\|TODO\|XXX" docs/          # no unresolved markers
   grep -rniE "5-state|7-state" docs/          # taxonomy must say 6-state
   ```

## Code Contributions (H0 Prototype Phase)

Once implementation begins:
- Branch naming: `feature/<short-description>`, `fix/<short-description>`, `docs/<short-description>`.
- Commit messages: [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`).
- Every PR touching `AI-004` (SIF Potential Engine) or `AI-005` (Barrier Analysis) logic must include or update tests per `docs/14_TESTING_STRATEGY.md`.
- Every new API endpoint must be documented in `docs/10_API_SPECIFICATION.md` in the same PR — undocumented endpoints will not be merged (this is exactly the class of gap `16_DOCUMENT_CONSISTENCY_AUDIT.md` FIX-10 addresses).

## Pull Request Process

1. Fork the repo and create your branch from `main`.
2. Fill out the PR template completely, including the consistency-impact checklist.
3. Ensure the Docs Lint CI workflow passes.
4. Request review from the relevant `CODEOWNERS` entry.
5. At least one approval is required before merge.

## Reporting Bugs / Requesting Features

Please use the issue templates under **Issues → New Issue**. For documentation inconsistencies specifically, use the **Documentation Inconsistency** template, which asks for the exact file/line evidence — see `docs/16_DOCUMENT_CONSISTENCY_AUDIT.md` §1 for why evidence-first reporting matters here.

## Code of Conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). By participating, you agree to uphold it.

## Questions

Open a [Discussion](../../discussions) or an issue tagged `question`.
