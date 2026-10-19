# FreshMargin - F&V Inventory & Finance Advisory POV

**Protecting margin without compromising availability.**

An independent, evidence-led case study exploring how demand signals, inventory risk, expiry exposure and financial decisions can be connected in a fresh-produce business.
## **[↗ OPEN THE LIVE INTERACTIVE DASHBOARD](https://freshmargin-fv-inventory-advisory-9zvcqhv9m7vw8qvn7hazkx.streamlit.app/)**

## What the app contains

1. **Executive Brief** — the business question, key findings, and evidence boundaries.
2. **Demand & Forecasts** — the existing 28-day demand baseline and its forecast-error caveat.
3. **Inventory & Expiry Risk** — simulated closing stock, batch ageing and projected expiry exposure.
4. **F&V Scenario Lab** — editable assumptions for stock, demand, usable life, markdown and simplified financial outcomes.
5. **Financial Impact** — a transparent scenario value bridge that separates assumed recovered value from intervention costs and trade-offs.
6. **Evidence & Recommendations** — limitations, evidence register and proposed validation / pilot steps.

## Key existing model outputs

- 1,437 food-product SKUs in the M5 inventory simulation.
- 67.40% WAPE for the existing recent-average demand baseline on the held-out evaluation period.
- 7,074 units in simulated closing inventory, valued at approximately $12,799.73 at modelled procurement cost.
- 404 units projected to remain unsold in the seven-day expiry scenario, representing approximately $1,104.32 in modelled inventory-cost exposure.

These are model outputs, not observed company performance, actual fresh-produce waste, realised losses or guaranteed savings.

## Data and limitations

- The M5 data covers US retail-food sales; it is not Swiggy data or actual F&V inventory data.
- Inventory, replenishment, procurement cost and shelf-life mechanics are simulated assumptions.
- The FreshRetailNet audit explored 4.5 million training records across 898 stores, 865 products and 18 cities. Its stockout figures are descriptive dataset observations, not company-specific estimates of lost sales. Category IDs are not translated into names.
- The F&V Scenario Lab and Financial Impact page are illustrative calculators, not forecasts or validated business cases.
- A 67.40% WAPE indicates substantial forecast error; the current baseline should not be used directly for live replenishment decisions.

## Run locally

Place this file beside the `outputs/` folder, then run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app resolves file paths relative to `app.py`, so it does not depend on a hard-coded Windows directory.

## Tools

Python, Pandas, Plotly, Streamlit, Jupyter Notebook.

## Portfolio positioning

A simulated business-finance case study demonstrating demand analysis, inventory modelling, cost-exposure estimation, reconciliation and decision support. It proposes hypotheses to validate; it does not claim measured savings or a proven company-specific problem.
