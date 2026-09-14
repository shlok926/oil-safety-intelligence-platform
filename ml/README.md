# ml/

**Status: Phase 1 Foundation Established (Interfaces & Cache Contracts).**

This directory contains the abstract pipeline interfaces (`ml/pipelines/interfaces.py`), offline model cache contracts (`ml/models/loader.py`), and domain schemas (`ml/rules/schemas.py`). Actual model weights, NLP processors, and SIF classifiers will be integrated in subsequent phases.

- AI architecture: [`../docs/08_AI_ARCHITECTURE.md`](../docs/08_AI_ARCHITECTURE.md)
- Data strategy & labeling (synthetic/prototype data policy): [`../docs/05_DATA_STRATEGY_AND_LABELING.md`](../docs/05_DATA_STRATEGY_AND_LABELING.md)
- Testing/evaluation methodology: [`../docs/14_TESTING_STRATEGY.md`](../docs/14_TESTING_STRATEGY.md)

**Reminder:** No real Oil India Limited (OIL) data may be committed to this
directory. Training/evaluation data must be synthetic or properly licensed
public data, per `../docs/01_PROJECT_CONSTITUTION.md` §16 and
`../docs/05_DATA_STRATEGY_AND_LABELING.md`. Model weight files must not be
committed directly — see `.gitignore` and use Git LFS or external artifact
storage once models exist.

See [`../docs/15_ROADMAP.md`](../docs/15_ROADMAP.md) for delivery phasing.
