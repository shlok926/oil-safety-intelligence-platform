---
name: Documentation Inconsistency
about: Report a contradiction, gap, or Constitution deviation between documents
title: "[DOCS] "
labels: documentation, consistency
assignees: ''
---

## What's Inconsistent?
Name the specific fact, ID, enum, or schema element in conflict.

## Evidence (required)
Give **exact file names and line numbers** for both sides of the conflict — evidence-first, per the standard set in `docs/16_DOCUMENT_CONSISTENCY_AUDIT.md` §1. Issues without concrete line citations will be asked for evidence before triage, since this project's history includes a prior audit draft that was rejected specifically for uncited claims.

**File A:**
```
path/to/file.md:LINE — exact quoted text
```

**File B:**
```
path/to/file.md:LINE — exact quoted text
```

## Which Side Is Correct?
If known, state which file should change and why (does one side match `01_PROJECT_CONSTITUTION.md`? does one side match `06_TECHNICAL_REQUIREMENTS.md`'s ID register?).

## Suggested Fix (optional)


## Verification Command
A `grep` (or similar) command a reviewer can run to confirm the issue and, later, confirm the fix:
```bash
grep -rn "TERM" docs/
```
