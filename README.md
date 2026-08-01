# SkyCity-Analytics-Dashboard
SkyCity Auckland Restaurants & Bars — Order Channel Performance and Market Share Analytics
# SkyCity Auckland — Channel Performance Analytics

**Order Channel Performance and Market Share Analytics for SkyCity Auckland Restaurants & Bars**

An end-to-end data analytics project analyzing order channel performance, market share, aggregator
dependency risk, and growth forecasting across 1,696 restaurant branches — built as part of the
Unified Mentor Data Analyst Internship program.

**Live Dashboard:** https://skycity-analytics-dashboard-sandeep-reddy.streamlit.app/

**Project Feedback Video:** https://drive.google.com/file/d/1cHOoiX8IJWJG_kiIrmPeZYXTRyPQA7k2/view?usp=sharing

---

## Overview

Auckland's hospitality market has shifted rapidly toward multi-channel ordering — In-Store dining,
Uber Eats, DoorDash, and Self-Delivery all now compete for the same customer. This project answers
three questions for restaurant operators and stakeholders:

1. How is order volume, revenue, and profit distributed across channels, subregions, cuisines, and
   business segments?
2. Which restaurants are most exposed to aggregator-dependence risk?
3. Given current growth trends, what does demand and profitability look like 3–12 months forward?

The project delivers three artifacts:

| Deliverable | Description |
|---|---|
| **Streamlit Dashboard** | Interactive, filterable dashboard with 7 modules and live KPI drill-downs |
| **Jupyter Notebook** | Fully executed EDA and forecasting methodology notebook |
| **Research Paper** | Formal write-up with embedded findings, insights, and recommendations, including an executive summary for government/policy stakeholders |

---

## Dashboard Features

### Core Modules
- **Executive Overview** — network-wide revenue/profit by channel, segment mix, profit-margin distribution, top restaurants
- **Channel Mix Overview** — order volume and market share by channel, in-store vs. delivery dominance, profit per order
- **Subregion Heatmaps** — channel share heatmap across Auckland's four subregions (CBD, North Shore, South Auckland, West Auckland)
- **Cuisine vs. Channel** — channel mix by cuisine type and business segment, aggregator-dependent cuisine ranking
- **Dependency Risk** — channel-risk profiling, diversification scoring, risk scatter plots
- **Growth Forecast** — adjustable 1–24 month compound-growth projection for orders, revenue, and profit
- **Restaurant Explorer** — searchable, sortable restaurant-level table with a projected 12-month value metric and a single-restaurant channel drill-down

### Interactive KPI Grid
Eight top-line KPIs (Total Orders, Revenue, Net Profit, Profit Margin, AOV, Aggregator Dependence,
Diversification Score, High-Risk Restaurants), each with:
- Live deltas vs. the full (unfiltered) network
- Hover/press micro-animations
- A click-to-expand breakdown popover with a supporting chart or gauge

### User Controls
- Subregion filter (multi-select)
- Cuisine type filter (multi-select)
- Restaurant segment filter (multi-select)
- Channel view toggle (All Channels / In-Store Only / Delivery Only)

---

## Tech Stack

- **Python** — pandas, NumPy for data processing
- **Streamlit** — dashboard framework
- **Plotly** — interactive charts (dashboard)
- **Matplotlib / Seaborn** — static charts (notebook)
- **Jupyter** — exploratory data analysis and forecasting methodology

---

## Project Structure

```
skycity-analytics-dashboard/
├── App.py                              # Streamlit dashboard application
├── requirements.txt                    # Python dependencies
├── assets/
│   ├── App_Logo.png                    # Brand logo (white, transparent)
│   ├── logo_badge.png                  # Logo badge for hero banner
│   └── hero_banner.jpg                 # Hero banner photography
├── data/
│   ├── SkyCity_Auckland_Restaurants_and_Bars.csv   # Raw source data
│   └── skycity_cleaned.csv             # Cleaned dataset with derived metrics
├── notebook/
│   └── SkyCity_Channel_Analytics.ipynb # Full EDA & forecasting methodology notebook
└── docs/
    └── SkyCity_Auckland_Research_Paper.pdf   # Research paper & executive summary
```

---

## Getting Started

### Prerequisites
- Python 3.9+
- pip

### Local Setup

```bash
# Clone the repository
git clone https://github.com/mSReddy46/SkyCity-Analytics-Dashboard.git
cd SkyCity-Analytics-Dashboard

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run App.py
```

The app will open at `http://localhost:8501`.

### Running the Notebook

```bash
pip install jupyter nbformat pandas numpy matplotlib seaborn
jupyter notebook notebook/SkyCity_Channel_Analytics.ipynb
```

---

## Dataset

The dataset (`SkyCity_Auckland_Restaurants_and_Bars.csv`) contains a monthly performance snapshot for
1,696 restaurant branches, with 30 columns spanning identity (restaurant, cuisine, segment, subregion),
order volume and revenue by channel, cost structure (COGS, OPEX, commission rates), and a per-restaurant
`GrowthFactor` used for forward projection. There is no separate transaction-level table — each row is
one restaurant's current monthly figures.

**Key columns:**

| Column | Description |
|---|---|
| `RestaurantID`, `RestaurantName` | Unique identifier and name |
| `CuisineType`, `Segment`, `Subregion` | Categorical descriptors |
| `MonthlyOrders`, `AOV` | Order volume and average order value |
| `{Channel}Orders`, `{Channel}Revenue`, `{Channel}NetProfit` | Per-channel figures for In-Store, Uber Eats, DoorDash, Self-Delivery |
| `CommissionRate`, `COGSRate`, `OPEXRate` | Cost structure |
| `GrowthFactor` | Month-over-month growth multiplier, used for forecasting |

> **Data quality note:** the source `InStoreShare`, `UE_share`, `DD_share`, and `SD_share` fields are
> on inconsistent bases (total-order share vs. delivery-only share) and do not sum to 100%. The
> dashboard and notebook both recompute all channel shares directly from the order-count columns to
> ensure consistency — see the notebook's Data Validation section and the research paper (Section 4.2)
> for full details.

---

## Methodology

The analysis follows a seven-step methodology, fully documented and executed in the Jupyter notebook:

1. Data Validation & Consistency Checks
2. Channel Volume Aggregation
3. Channel Market Share Analysis
4. Geographic Channel Preference Analysis
5. Cuisine & Segment Channel Patterns
6. Channel Dependency Risk Identification
7. Growth & Demand Forecasting (compound growth projection using `GrowthFactor`)

---

## Key Findings

- Delivery channels account for **82.5%** of all orders network-wide; Uber Eats alone holds **39.6%** market share.
- Aggregator orders (Uber Eats, DoorDash) return **$0.32–$0.35** profit per order, versus **$8.82–$10.31** for Self-Delivery and In-Store — a **25–30x** profitability gap driven by 28–33% commission rates.
- **603 restaurants (35.6%)** exceed 70% combined Uber Eats + DoorDash dependence, the network's primary channel-risk signal.
- Network-wide 6-month order growth is projected at **+19.3%**, concentrated in the same aggregator channels driving today's risk profile.

Full findings, insights, and recommendations — including a section for government/regulatory
stakeholders — are documented in `SkyCity_Auckland_Research_Paper.pdf`.

---

## Acknowledgments

This project was completed as part of the **Unified Mentor Data Analyst Internship** program. It
builds directly on feedback from a prior internship project (APL Logistics profitability dashboard),
which recommended adding predictive analytics and drill-down functionality — both implemented here.

---

## Author

**M. Sandeep Reddy**
Data Analyst Intern, Unified Mentor
