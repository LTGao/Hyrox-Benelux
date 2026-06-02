# HYROX Benelux · Market Intelligence Report

A data-driven case study analysing five seasons of HYROX race results across seven Benelux cities — built to demonstrate audience insight and digital marketing strategy for the Benelux sports market.

**[→ View Report](https://ltgao.github.io/Hyrox-Benelux)**

---

## What's in it

**74,645 participants · 17 events · 7 cities · Seasons 4–8 · 2021–2026**

Cities covered: Amsterdam, Rotterdam, Maastricht, Utrecht, Heerenveen (NL) and Gent, Mechelen (BE).

The report covers:
- **The Market** — participation growth per event and season, shown on an interactive cumulative map of all seven cities
- **The Audience** — gender, age, nationality and athletic-level breakdown (dedicated `audience.html` page)
- **Participation Loyalty** — cross-season retention from 61,661 uniquely named athletes
- **The Opportunity** — converting audience-ticket spectators into participants
- **The Campaigns** — two data-backed campaign concepts (acquisition + retention) with full email flows and paid/SEO ideas
- **Book a Demo / Contact** — a working booking form (Web3Forms) on a dedicated `contact.html` page

---

## Data sources

| Dataset | Coverage | Source |
|---|---|---|
| `hyrox_results s4-6.csv` | Global, Seasons 4–6, 92k rows | [Kaggle](https://www.kaggle.com/) |
| `hyrox_benelux_s7_s8.csv` | Benelux only, Seasons 7–8 | HYROX official results (scraped) |
| `hyrox_benelux_s4_s6_named.csv` | Benelux only, Seasons 4–6, with athlete names | HYROX official results (scraped) |

The S4–S6 Kaggle file was filtered to Benelux events, and all seasons were additionally scraped from the HYROX platform to obtain athlete names for cross-season retention analysis. Previously unreported events in Heerenveen, Gent and Mechelen were added.

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
├── index.html                  # Single-page report (Chart.js + Leaflet map)
├── audience.html               # Detailed audience profile page
├── contact.html                # Book a demo / contact page (Web3Forms)
├── images/                     # Photography
├── data/
│   └── dashboard_data.js       # Pre-aggregated data for charts
└── generate_dashboard_data.py  # Python script to rebuild data from CSV
```

---

## Built by

**Leiting Gao** — Digital marketer based in the Netherlands, sports industry background.
Built as a case study for a digital marketing role application in Benelux.

- Python (pandas) for data merging, scraping and aggregation
- Chart.js for charts, Leaflet for the interactive city map
- Web3Forms for the contact form
- Vanilla HTML/CSS — no build tools, deploys directly via GitHub Pages

[LinkedIn](https://www.linkedin.com/in/leiting-gao/) · gaoleiting@hotmail.com
