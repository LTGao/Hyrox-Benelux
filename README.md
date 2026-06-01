# HYROX Benelux · Market Intelligence Dashboard

A data-driven case study analysing five seasons of HYROX race results across Amsterdam, Rotterdam, Maastricht, and Utrecht — built to demonstrate audience insight and digital marketing strategy for the Benelux sports market.

**[→ View Live Dashboard](https://ltgao.github.io/Hyrox-Benelux)**

---

## What's in it

**52,647 participants · 12 events · Seasons 4–8 · 2021–2026**

The dashboard covers:
- Participation growth per event and season
- Gender split evolution (S4 → S8)
- Top 15 nationalities with local vs. international breakdown
- Age group distribution by gender
- Finish time distribution (open division)
- Division breakdown (open / doubles / pro / relay)
- Audience personas derived from the data
- Data-backed campaign concepts
- Strategic insights for the Benelux market

---

## Data sources

| Dataset | Coverage | Source |
|---|---|---|
| `hyrox_results s4-6.csv` | Global, Seasons 4–6, 92k rows | [Kaggle](https://www.kaggle.com/) |
| `hyrox_benelux_s7_s8.csv` | Benelux only, Seasons 7–8, 45k rows | HYROX official results (scraped) |

The S4–S6 file was filtered to Benelux events only (Amsterdam, Rotterdam, Maastricht, Utrecht) before merging.

---

## How to run locally

**1. Install dependencies**
```bash
pip install pandas
```

**2. Regenerate the dashboard data**
```bash
python generate_dashboard_data.py
```
This reads the merged CSV and writes `data/dashboard_data.js`.

**3. Serve locally**
```bash
python -m http.server 8000
```
Then open `http://localhost:8000`.

---

## Project structure

```
Hyrox-Benelux/
├── index.html                  # Single-page dashboard (Chart.js)
├── data/
│   └── dashboard_data.js       # Pre-aggregated data for charts
└── generate_dashboard_data.py  # Python script to rebuild data from CSV
```

---

## Built by

**LT Gao** — Digital marketer based in the Netherlands (10 years), sports industry background.  
Built as a case study for a digital marketing role application in Benelux.

- Python (pandas) for data merging and aggregation
- Chart.js for visualisation
- Vanilla HTML/CSS — no build tools, deploys directly via GitHub Pages
