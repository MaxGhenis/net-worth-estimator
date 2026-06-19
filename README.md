# Assumption Ledger

A Streamlit app for estimating net worth from dated, uncertain wealth drivers.

Most net-worth calculators stop at current assets minus liabilities. This app is
for harder cases: founders, executives, public figures, inherited wealth, and
anyone whose wealth depends on dated liquidity events, taxes, vesting, spending,
portfolio returns, and source quality.

## Model

The app separates:

- liquidity events: deal value, ownership range, keep rate, return multiple
- compensation streams: annual gross comp, investable share, compounding return
- current assets and liabilities
- global haircut for spending, philanthropy, errors, and unmodeled leakage
- source confidence and audit notes

Outputs include low/base/high estimates, driver contribution, sensitivity
spread, evidence mix, and threshold analysis.

## Run

```bash
uv venv --python 3.13
uv pip install -r requirements.txt
uv run streamlit run app.py
```

## Test

```bash
uv run python -m unittest discover -s tests -v
```

## Notes

The bundled sample is a founder/executive-style model based on public deal
evidence and analyst assumptions. It is a scenario model, not a verified
personal balance sheet.
