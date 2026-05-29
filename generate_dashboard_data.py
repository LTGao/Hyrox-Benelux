"""
Generate dashboard JSON data from merged HYROX Benelux dataset.
Run once to produce data/dashboard_data.js (embedded JS module).
"""
import json
from pathlib import Path
import pandas as pd

BASE = Path(__file__).parent
DATA_DIR = BASE / "data"
DATA_DIR.mkdir(exist_ok=True)

SOURCE = Path(r"D:\Tool\Claude Code\Projects\WSL\hyrox_analysis\hyrox_benelux_s4_s8_clean.csv")

df = pd.read_csv(SOURCE, low_memory=False)

# ── Normalise ────────────────────────────────────────────────────────────────
for col in ["gender", "division", "location", "nationality", "age_group"]:
    df[col] = df[col].astype(str).str.strip().str.lower()

df["nationality"] = df["nationality"].str.upper()
df["season"] = df["season"].astype(str).str.replace(r"\.0$", "", regex=True)
df["total_time"] = pd.to_numeric(df["total_time"], errors="coerce")

# Add year from event_name
def extract_year(ev):
    import re
    m = re.search(r"\b(20\d\d)\b", str(ev))
    return int(m.group(1)) if m else None

df["year"] = df["event_name"].apply(extract_year)

# Canonical event label: "S4 · Amsterdam 2021"
SEASON_YEAR = {
    "4": "2021–22", "5": "2022–23", "6": "2023–24",
    "7": "2024–25", "8": "2025–26",
}
LOC_LABEL = {
    "amsterdam": "Amsterdam", "rotterdam": "Rotterdam",
    "maastricht": "Maastricht", "utrecht": "Utrecht",
}

def event_label(row):
    loc = LOC_LABEL.get(row["location"], row["location"].title())
    return f"S{row['season']} {loc} {row['year']}"

df["event_label"] = df.apply(event_label, axis=1)

# Sort key for events
EVENT_ORDER = [
    "S4 Amsterdam 2021", "S4 Maastricht 2022",
    "S5 Amsterdam 2022", "S5 Rotterdam 2023", "S5 Maastricht 2023",
    "S6 Amsterdam 2023",
    "S7 Amsterdam 2024", "S7 Rotterdam 2025", "S7 Maastricht 2025",
    "S8 Amsterdam 2026", "S8 Rotterdam 2026", "S8 Utrecht 2025",
]

events_sorted = (
    df.groupby(["season", "location", "year", "event_label"])
    .size().reset_index(name="n")
    .sort_values(["season", "year", "location"])
)

# ── 1. Participation per event ────────────────────────────────────────────────
participation = []
for _, row in events_sorted.iterrows():
    participation.append({
        "event": row["event_label"],
        "season": row["season"],
        "location": row["location"],
        "year": int(row["year"]) if pd.notna(row["year"]) else None,
        "participants": int(row["n"]),
    })

# ── 2. Growth summary ─────────────────────────────────────────────────────────
by_season = df.groupby("season").size().reset_index(name="n").sort_values("season")
growth = [{"season": f"S{r['season']}", "participants": int(r["n"])} for _, r in by_season.iterrows()]

# ── 3. Gender split per season ────────────────────────────────────────────────
gender_season = (
    df[df["gender"].isin(["male", "female"])]
    .groupby(["season", "gender"]).size().unstack(fill_value=0).reset_index()
)
gender_data = []
for _, row in gender_season.iterrows():
    gender_data.append({
        "season": f"S{row['season']}",
        "male": int(row.get("male", 0)),
        "female": int(row.get("female", 0)),
    })

# ── 4. Top nationalities ──────────────────────────────────────────────────────
nat_counts = (
    df[df["nationality"].str.len() == 3]
    .groupby("nationality").size().reset_index(name="n")
    .sort_values("n", ascending=False).head(15)
)
nationality_data = [
    {"country": r["nationality"], "participants": int(r["n"])}
    for _, r in nat_counts.iterrows()
]

# Local (NL+BE+LU) vs International
local = {"NLD", "BEL", "LUX"}
df["is_local"] = df["nationality"].isin(local)
local_pct = round(df["is_local"].mean() * 100, 1)
intl_pct = round(100 - local_pct, 1)

# Nationality trend by season (top 5 countries)
top5 = [r["country"] for r in nationality_data[:5]]
nat_trend_raw = (
    df[df["nationality"].isin(top5)]
    .groupby(["season", "nationality"]).size().unstack(fill_value=0)
)
nat_trend = {"seasons": [f"S{s}" for s in nat_trend_raw.index.tolist()]}
for c in top5:
    nat_trend[c] = nat_trend_raw[c].tolist() if c in nat_trend_raw.columns else []

# ── 5. Age group distribution ─────────────────────────────────────────────────
AGE_ORDER = ["18-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60+"]
age_counts = (
    df[df["age_group"].isin([a.lower() for a in AGE_ORDER])]
    .groupby("age_group").size()
)
age_data = []
for ag in AGE_ORDER:
    age_data.append({
        "age_group": ag,
        "participants": int(age_counts.get(ag.lower(), 0)),
    })

# Age by gender
age_gender_raw = (
    df[df["gender"].isin(["male", "female"]) & df["age_group"].isin([a.lower() for a in AGE_ORDER])]
    .groupby(["age_group", "gender"]).size().unstack(fill_value=0)
)
age_gender = {"age_groups": AGE_ORDER}
for g in ["male", "female"]:
    age_gender[g] = [int(age_gender_raw.get(g, pd.Series()).get(ag.lower(), 0)) for ag in AGE_ORDER]

# ── 6. Median finish time (open division) per event ───────────────────────────
open_df = df[
    (df["division"] == "open") &
    df["total_time"].notna() &
    (df["total_time"] > 40) &
    (df["total_time"] < 180)
]
time_by_event = (
    open_df.groupby(["event_label", "gender"])["total_time"]
    .agg(["median", lambda x: x.quantile(0.25), lambda x: x.quantile(0.75)])
    .reset_index()
)
time_by_event.columns = ["event", "gender", "median", "q25", "q75"]

# Get sorted event list from participation
event_order_actual = [p["event"] for p in participation]
time_data = {"events": event_order_actual, "male": [], "female": []}
for ev in event_order_actual:
    for g in ["male", "female"]:
        row = time_by_event[(time_by_event["event"] == ev) & (time_by_event["gender"] == g)]
        if len(row):
            time_data[g].append({
                "median": round(float(row["median"].iloc[0]), 1),
                "q25": round(float(row["q25"].iloc[0]), 1),
                "q75": round(float(row["q75"].iloc[0]), 1),
            })
        else:
            time_data[g].append(None)

# ── 7. Division breakdown overall ────────────────────────────────────────────
div_counts = df.groupby("division").size().reset_index(name="n").sort_values("n", ascending=False)
division_data = [
    {"division": r["division"].replace("_", " ").title(), "participants": int(r["n"])}
    for _, r in div_counts.iterrows()
]

# ── 8. Location breakdown ─────────────────────────────────────────────────────
loc_counts = df.groupby("location").size().reset_index(name="n").sort_values("n", ascending=False)
location_data = [
    {"location": LOC_LABEL.get(r["location"], r["location"].title()), "participants": int(r["n"])}
    for _, r in loc_counts.iterrows()
]

# ── 9. Key KPIs ───────────────────────────────────────────────────────────────
total = len(df)
unique_nationalities = int(df[df["nationality"].str.len() == 3]["nationality"].nunique())
s4_total = int(by_season[by_season["season"] == "4"]["n"].sum()) if "4" in by_season["season"].values else 0
s8_total = int(by_season[by_season["season"] == "8"]["n"].sum()) if "8" in by_season["season"].values else 0
growth_multiple = round(s8_total / s4_total, 1) if s4_total else 0

male_pct = round(df[df["gender"] == "male"].shape[0] / total * 100)
female_pct = 100 - male_pct

kpis = {
    "total_participants": total,
    "unique_nationalities": unique_nationalities,
    "events_covered": int(events_sorted.shape[0]),
    "seasons_covered": 5,
    "season_range": "2021–2026",
    "growth_multiple": growth_multiple,
    "local_pct": local_pct,
    "intl_pct": intl_pct,
    "male_pct": male_pct,
    "female_pct": female_pct,
}

# ── 10. Time histogram (open division, all events combined) ──────────────────
hist_bins = list(range(50, 175, 5))
male_hist, _ = pd.cut(
    open_df[open_df["gender"] == "male"]["total_time"],
    bins=hist_bins, retbins=False, right=False
).value_counts(sort=False).align(
    pd.cut(open_df[open_df["gender"] == "male"]["total_time"], bins=hist_bins, right=False)
    .value_counts(sort=False)
)
# simpler approach
def hist_data(series, bins):
    counts = []
    labels = []
    for i in range(len(bins) - 1):
        lo, hi = bins[i], bins[i+1]
        counts.append(int(((series >= lo) & (series < hi)).sum()))
        labels.append(f"{lo}–{hi}")
    return labels, counts

male_series = open_df[open_df["gender"] == "male"]["total_time"].dropna()
female_series = open_df[open_df["gender"] == "female"]["total_time"].dropna()
hist_labels, male_hist_counts = hist_data(male_series, hist_bins)
_, female_hist_counts = hist_data(female_series, hist_bins)

time_histogram = {
    "labels": hist_labels,
    "male": male_hist_counts,
    "female": female_hist_counts,
}

# ── Assemble & write ──────────────────────────────────────────────────────────
dashboard = {
    "kpis": kpis,
    "participation": participation,
    "growth": growth,
    "gender": gender_data,
    "nationality": nationality_data,
    "nat_trend": nat_trend,
    "top5_countries": top5,
    "age": age_data,
    "age_gender": age_gender,
    "finish_time": time_data,
    "time_histogram": time_histogram,
    "division": division_data,
    "location": location_data,
}

out = DATA_DIR / "dashboard_data.js"
out.write_text(
    "const DASHBOARD_DATA = " + json.dumps(dashboard, indent=2, ensure_ascii=False) + ";\n",
    encoding="utf-8"
)
print(f"Written {out}  ({out.stat().st_size // 1024} KB)")
print(f"KPIs: {kpis}")
