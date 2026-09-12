## Summary

<!-- What does this PR do, in 1-3 sentences? -->

## Type of Change

- [ ] Documentation update
- [ ] New feature (code)
- [ ] Bug fix (code)
- [ ] Refactor (no behavior change)
- [ ] Consistency fix (cross-document alignment)

## Related Issue(s)

Closes #

## Consistency & Constitution Checklist

- [ ] I have read `docs/01_PROJECT_CONSTITUTION.md` and this change does not contradict it.
- [ ] If this PR adds/changes a requirement ID (`FR-`, `AI-`, `UX-`, `HIL-`, `DATA-`, `SEC-`, `NFR-`, `OBS-`), it is registered/updated in `docs/06_TECHNICAL_REQUIREMENTS.md`.
- [ ] If this PR adds/changes an enum, table name, or field name, I grepped `/docs` for existing usages and updated all occurrences:
  ```bash
  grep -rn "YOUR_TERM" docs/
  ```
- [ ] No fabricated OIL statistics, accuracy figures, or claims of official endorsement/deployment were introduced.
- [ ] All new synthetic/example data is explicitly labelled as such (`[ILLUSTRATIVE EXAMPLE]` / `[PROTOTYPE ASSUMPTION]`).
- [ ] If this PR adds a new API endpoint, it is documented in `docs/10_API_SPECIFICATION.md` in this same PR.
- [ ] If this PR touches the SIF Potential Engine (`AI-004`) or Barrier Analysis (`AI-005`), corresponding tests/test-cases are added or updated per `docs/14_TESTING_STRATEGY.md`.

## How Was This Tested?

<!-- For docs-only PRs: describe the grep/manual cross-check performed. For code PRs: describe test coverage. -->

## Screenshots (if UI-related)

<!-- Optional -->

## Additional Notes

<!-- Anything reviewers should know -->
