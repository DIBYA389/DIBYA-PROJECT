# ECL Calculator

A Streamlit app that computes Expected Credit Loss (ECL) from Probability
of Default (PD), Loss Given Default (LGD), and Exposure at Default (EAD)
inputs, using the standard formula:

```
ECL = PD x LGD x EAD
```

## Project structure

```
data/
  pd_sample.csv    Sample PD per account ID
  lgd_sample.csv   Sample LGD per account ID
  ead_sample.csv   Sample EAD per account ID
scripts/
  generate_sample_data.py   Regenerates the sample CSVs from UCI_Credit_Card.csv
app.py             Streamlit app
requirements.txt   Python dependencies
UCI_Credit_Card.csv  Source dataset used to derive the sample data
```

The sample files are derived from `UCI_Credit_Card.csv` (500 accounts):
PD is modeled from each account's payment-delinquency history and prior
default flag, LGD is drawn from a beta distribution typical of unsecured
retail credit, and EAD is the current bill utilization capped at the
credit limit. Regenerate them anytime with:

```
python scripts/generate_sample_data.py
```

## Setup

Create and activate a virtual environment, then install dependencies.

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**macOS/Linux:**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

Open the URL Streamlit prints (defaults to http://localhost:8501).

## Usage

- Use the sidebar to upload your own PD, LGD, and EAD CSV files (each
  needs an `ID` column plus the corresponding value column), or leave
  them blank to use the bundled sample data.
- The app merges the three inputs on `ID`, computes ECL per account, and
  shows summary metrics, a sortable detail table, an ECL distribution
  chart, and the top 10 exposures by ECL.
- Download the merged results as CSV from the button at the bottom.
