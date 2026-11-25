# Contributing

This repo is a template; project files live in your own copy. To contribute to the template:

1. For a rule suggestion or a bug, open an issue first (use the templates).
2. Do not change rule IDs (e.g. `LAY-23`); a new rule gets a new number.
3. Every change updates the English `README.md`, the Turkish `README.tr.md` and `CHANGELOG.md`; the version lines must match (`check_repo.py` checks this).
4. Run locally before submitting:

```bash
python -m unittest discover -s tests
python scripts/check_repo.py
```

5. When adding a datasheet, CAD model or logo, you must have a license/redistribution permission. Do not add confidential information, API keys or customer designs.
