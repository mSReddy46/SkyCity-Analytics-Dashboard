"""
SkyCity Auckland Restaurants & Bars
Order Channel Performance and Market Share Analytics — Streamlit Dashboard

"""

import base64
import os

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# =====================================================================
# PAGE CONFIG
# =====================================================================
APP_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(APP_DIR, "assets", "App_Logo.png")
LOGO_BADGE_PATH = os.path.join(APP_DIR, "assets", "logo_badge.png")
HERO_BANNER_PATH = os.path.join(APP_DIR, "assets", "hero_banner.jpg")

st.set_page_config(
    page_title="SkyCity Auckland | Channel Performance Analytics",
    page_icon=LOGO_PATH if os.path.exists(LOGO_PATH) else "📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

GOLD = "#B48D30"
GOLD_LIGHT = "#D4AF5A"
INK = "#0B0B0B"
CHARCOAL = "#1A1A1A"
CARD_BG = "#151515"

CHANNEL_COLORS = {
    "In-Store": "#9CA3AF",
    "Uber Eats": "#06C167",
    "DoorDash": "#FF3008",
    "Self-Delivery": GOLD_LIGHT,
}

PLOTLY_TEMPLATE = "plotly_dark"


def style_fig(fig, height=420):
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E5E5E5"),
        height=height,
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    return fig


def img_to_b64(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


LOGO_B64 = img_to_b64(LOGO_PATH)
LOGO_BADGE_B64 = img_to_b64(LOGO_BADGE_PATH)
HERO_BANNER_B64 = img_to_b64(HERO_BANNER_PATH)

# =====================================================================
# GLOBAL CSS — brand blending (gold / black / charcoal)
# =====================================================================
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: #0E0E10;
        color: #EDEDED;
    }}
    section[data-testid="stSidebar"] {{
        background-color: {INK};
        border-right: 1px solid #2A2A2A;
    }}
    section[data-testid="stSidebar"] * {{
        color: #EDEDED !important;
    }}
    .hero {{
        position: relative;
        height: 280px;
        border-radius: 16px;
        overflow: hidden;
        margin-bottom: 24px;
        border: 1px solid #2A2415;
        box-shadow: 0 6px 32px rgba(180,141,48,0.14);
    }}
    .hero-photo {{
        position: absolute; top: 0; left: 0; right: 0; bottom: 0;
        width: 100%; height: 100%;
        background-repeat: no-repeat;
        background-size: cover;
        background-position: center 50%;
    }}
    .hero-scrim {{
        position: absolute; top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(100deg, rgba(2,2,2,0.80) 0%, rgba(2,2,2,0.55) 30%, rgba(2,2,2,0.20) 55%, rgba(2,2,2,0.06) 78%),
                    linear-gradient(180deg, rgba(2,2,2,0.10) 0%, rgba(2,2,2,0.05) 45%, rgba(2,2,2,0.55) 100%);
    }}
    .hero-logo-chip {{
        position: absolute; top: 20px; left: 24px; z-index: 3;
        display: flex; align-items: center;
        padding: 9px 16px;
        background: rgba(8,8,8,0.55);
        border: 1px solid rgba(180,141,48,0.45);
        border-radius: 9px;
        backdrop-filter: blur(3px);
    }}
    .hero-logo-chip img {{
        height: 32px; width: auto;
    }}
    .hero-textblock {{
        position: absolute; left: 26px; bottom: 24px; right: 26px; z-index: 3;
    }}
    .hero-textblock h1 {{
        font-size: 26px; margin:0; color: #FFFFFF; font-weight: 800; letter-spacing: 0.3px; line-height:1.25;
        text-shadow: 0 2px 12px rgba(0,0,0,0.9);
    }}
    .hero-textblock p {{
        margin:8px 0 0 0; color: {GOLD_LIGHT}; font-size: 12.5px; letter-spacing: 1.6px; text-transform: uppercase;
        font-weight: 600; text-shadow: 0 2px 8px rgba(0,0,0,0.9);
    }}
    div[data-testid="stMetric"] {{
        background-color: {CARD_BG};
        border: 1px solid #2A2A2A;
        border-left: 3px solid {GOLD};
        border-radius: 10px;
        padding: 14px 16px 10px 16px;
        cursor: pointer;
        transition: transform 0.15s ease, box-shadow 0.2s ease, border-color 0.2s ease, background-color 0.2s ease;
    }}
    div[data-testid="stMetric"]:hover {{
        transform: translateY(-4px) scale(1.015);
        box-shadow: 0 10px 22px rgba(180,141,48,0.28);
        border-color: {GOLD};
        border-left: 3px solid {GOLD_LIGHT};
        background-color: #1B1B1B;
    }}
    div[data-testid="stMetric"]:active {{
        transform: translateY(-1px) scale(0.965);
        box-shadow: 0 3px 8px rgba(180,141,48,0.4) inset;
        border-left: 3px solid #F0C674;
        transition: transform 0.06s ease, box-shadow 0.06s ease;
    }}
    div[data-testid="stMetricValue"] {{ transition: color 0.15s ease; }}
    div[data-testid="stMetric"]:hover div[data-testid="stMetricValue"] {{ color: #F0C674 !important; }}
    div[data-testid="stMetricLabel"] {{ color: #B9B9B9 !important; font-size: 12.5px !important; }}
    div[data-testid="stMetricValue"] {{ color: {GOLD_LIGHT} !important; }}
    .section-card {{
        background-color: {CARD_BG};
        border: 1px solid #2A2A2A;
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 16px;
    }}
    .section-card h4 {{ color: {GOLD_LIGHT}; margin-top:0; }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 4px; }}
    .stTabs [data-baseweb="tab"] {{
        background-color: {CARD_BG}; border-radius: 8px 8px 0 0; color: #C9C9C9; padding: 8px 18px;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {GOLD} !important; color: #111 !important; font-weight: 600;
    }}
    .risk-badge {{
        display:inline-block; padding: 3px 10px; border-radius: 20px; font-size: 12px; font-weight:600;
    }}
    .footer-note {{ color:#7A7A7A; font-size:12px; text-align:center; margin-top: 30px; }}
    div[data-testid="stPopoverBody"] {{
        background-color: {CARD_BG} !important;
        border: 1px solid {GOLD} !important;
    }}
    button[data-testid="stPopoverButton"] {{
        background-color: transparent !important;
        border: 1px solid #3A3A3A !important;
        color: {GOLD_LIGHT} !important;
        font-size: 12px !important;
        padding: 2px 10px !important;
        margin-top: -6px !important;
    }}
    button[data-testid="stPopoverButton"]:hover {{
        border-color: {GOLD} !important;
        color: #FFF !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# =====================================================================
# DATA LOADING
# =====================================================================
@st.cache_data
def load_data():
    cleaned_path = os.path.join(APP_DIR, "data", "skycity_cleaned.csv")
    raw_path = os.path.join(APP_DIR, "data", "SkyCity_Auckland_Restaurants_and_Bars.csv")

    if os.path.exists(cleaned_path):
        df = pd.read_csv(cleaned_path)
    else:
        df = pd.read_csv(raw_path)
        df["DeliveryOrders"] = df["UberEatsOrders"] + df["DoorDashOrders"] + df["SelfDeliveryOrders"]
        df["TotalRevenue"] = (
            df["InStoreRevenue"] + df["UberEatsRevenue"] + df["DoorDashRevenue"] + df["SelfDeliveryRevenue"]
        )
        df["TotalNetProfit"] = (
            df["InStoreNetProfit"] + df["UberEatsNetProfit"] + df["DoorDashNetProfit"] + df["SelfDeliveryNetProfit"]
        )
        df["ProfitMargin"] = df["TotalNetProfit"] / df["TotalRevenue"]
        df["InStoreShare_calc"] = df["InStoreOrders"] / df["MonthlyOrders"]
        df["UE_share_total"] = df["UberEatsOrders"] / df["MonthlyOrders"]
        df["DD_share_total"] = df["DoorDashOrders"] / df["MonthlyOrders"]
        df["SD_share_total"] = df["SelfDeliveryOrders"] / df["MonthlyOrders"]
        df["AggregatorDependenceIndex"] = df["UE_share_total"] + df["DD_share_total"]
        share_cols = ["InStoreShare_calc", "UE_share_total", "DD_share_total", "SD_share_total"]
        hhi = (df[share_cols] ** 2).sum(axis=1)
        n = len(share_cols)
        df["DiversificationScore"] = 1 - (hhi - 1 / n) / (1 - 1 / n)

    df["CommissionCost"] = (df["UberEatsRevenue"] + df["DoorDashRevenue"]) * df["CommissionRate"]
    return df


df = load_data()

CHANNEL_ORDER_COLS = {
    "In-Store": "InStoreOrders",
    "Uber Eats": "UberEatsOrders",
    "DoorDash": "DoorDashOrders",
    "Self-Delivery": "SelfDeliveryOrders",
}
CHANNEL_REVENUE_COLS = {
    "In-Store": "InStoreRevenue",
    "Uber Eats": "UberEatsRevenue",
    "DoorDash": "DoorDashRevenue",
    "Self-Delivery": "SelfDeliveryRevenue",
}
CHANNEL_PROFIT_COLS = {
    "In-Store": "InStoreNetProfit",
    "Uber Eats": "UberEatsNetProfit",
    "DoorDash": "DoorDashNetProfit",
    "Self-Delivery": "SelfDeliveryNetProfit",
}

# =====================================================================
# SIDEBAR — brand + filters (User Capabilities)
# =====================================================================
with st.sidebar:
    if LOGO_B64:
        st.markdown(
            f"<div style='text-align:center;margin-bottom:6px;padding:10px 0;'>"
            f"<img src='data:image/png;base64,{LOGO_B64}' style='width:80%;'/></div>",
            unsafe_allow_html=True,
        )
    st.markdown(
        f"<p style='text-align:center;color:{GOLD_LIGHT};letter-spacing:1px;font-size:12px;"
        f"text-transform:uppercase;margin-top:-6px;'>Order Channel Performance & Market Share Analytics</p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown("### 💠 User Filters")

    subregions = sorted(df["Subregion"].unique())
    sel_subregions = st.multiselect("Subregion", subregions, default=subregions)

    cuisines = sorted(df["CuisineType"].unique())
    sel_cuisines = st.multiselect("Cuisine Type", cuisines, default=cuisines)

    segments = sorted(df["Segment"].unique())
    sel_segments = st.multiselect("Restaurant Segment", segments, default=segments)

    st.markdown("### 🔀 Channel View")
    channel_toggle = st.radio(
        "Order type",
        ["All Channels", "In-Store Only", "Delivery Only"],
        index=0,
        help="Toggle between in-store (walk-in) and delivery (Uber Eats + DoorDash + Self-Delivery) order flow.",
    )

    st.markdown("---")
    st.caption(f"Restaurants in view: **{len(df):,}** total in dataset")

# --- Apply filters ---
fdf = df[
    df["Subregion"].isin(sel_subregions)
    & df["CuisineType"].isin(sel_cuisines)
    & df["Segment"].isin(sel_segments)
].copy()

if fdf.empty:
    st.warning("No restaurants match the selected filters. Please broaden your selection.")
    st.stop()

# Determine active channel set based on toggle
if channel_toggle == "In-Store Only":
    active_channels = ["In-Store"]
elif channel_toggle == "Delivery Only":
    active_channels = ["Uber Eats", "DoorDash", "Self-Delivery"]
else:
    active_channels = ["In-Store", "Uber Eats", "DoorDash", "Self-Delivery"]

order_cols_active = [CHANNEL_ORDER_COLS[c] for c in active_channels]
revenue_cols_active = [CHANNEL_REVENUE_COLS[c] for c in active_channels]
profit_cols_active = [CHANNEL_PROFIT_COLS[c] for c in active_channels]

fdf["ViewOrders"] = fdf[order_cols_active].sum(axis=1)
fdf["ViewRevenue"] = fdf[revenue_cols_active].sum(axis=1)
fdf["ViewProfit"] = fdf[profit_cols_active].sum(axis=1)

# =====================================================================
# HERO HEADER (brand blending) — compact single photo banner,
# logo chip + title/subtitle overlaid directly on the photo
# =====================================================================
logo_chip_html = (
    f"<div class='hero-logo-chip'><img src='data:image/png;base64,{LOGO_BADGE_B64}'/></div>"
    if LOGO_BADGE_B64 else ""
)
hero_photo_html = (
    f"<div class='hero-photo' style=\"background-image:url('data:image/jpeg;base64,{HERO_BANNER_B64}')\"></div>"
    if HERO_BANNER_B64 else ""
)

st.markdown(
    f"""
    <div class="hero">
        {hero_photo_html}
        <div class="hero-scrim"></div>
        {logo_chip_html}
        <div class="hero-textblock">
            <h1>SkyCity Auckland</h1>
            <p>Order Channel Performance & Market Share Analytics · Executive Intelligence Dashboard</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =====================================================================
# TOP-LINE INTERACTIVE KPI GRID
# (metrics with live deltas vs. the full network + click-to-expand
#  breakdown popovers, in the spirit of the APL Logistics dashboard)
# =====================================================================
total_orders = fdf["ViewOrders"].sum()
total_revenue = fdf["ViewRevenue"].sum()
total_profit = fdf["ViewProfit"].sum()
margin = (total_profit / total_revenue * 100) if total_revenue else 0
avg_aov = fdf["AOV"].mean()
agg_dep = fdf["AggregatorDependenceIndex"].mean() * 100
div_score = fdf["DiversificationScore"].mean()
high_risk_ct = (fdf["AggregatorDependenceIndex"] > 0.70).sum()

# Baseline = full, unfiltered network (all channels) — deltas show how the
# current filter selection compares to the overall SkyCity Auckland network.
base_orders = df["MonthlyOrders"].sum()
base_revenue = df["TotalRevenue"].sum()
base_profit = df["TotalNetProfit"].sum()
base_margin = (base_profit / base_revenue * 100) if base_revenue else 0
base_aov = df["AOV"].mean()
base_agg_dep = df["AggregatorDependenceIndex"].mean() * 100
base_div = df["DiversificationScore"].mean()
base_high_risk_ct = (df["AggregatorDependenceIndex"] > 0.70).sum()


def _hex_to_rgba(hex_color, alpha=0.25):
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def gauge_fig(value, title, max_val=100, zones=((0, 50, "#10B981"), (50, 70, "#F59E0B"), (70, 100, "#EF4444")), suffix="%"):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number={"suffix": suffix, "font": {"color": GOLD_LIGHT, "size": 30}},
            gauge={
                "axis": {"range": [0, max_val], "tickcolor": "#888", "tickfont": {"color": "#999"}},
                "bar": {"color": GOLD_LIGHT, "thickness": 0.35},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 0,
                "steps": [{"range": [z[0], z[1]], "color": _hex_to_rgba(z[2], 0.28)} for z in zones],
            },
            title={"text": title, "font": {"size": 13, "color": "#CCCCCC"}},
        )
    )
    fig.update_layout(height=210, margin=dict(l=25, r=25, t=45, b=10), paper_bgcolor="rgba(0,0,0,0)", font={"color": "#EEE"})
    return fig


def pct_delta(current, base):
    if base:
        return (current - base) / abs(base) * 100
    return 0.0


kpi_row1 = st.columns(4)
kpi_row2 = st.columns(4)

# --- 1. Total Orders ---
with kpi_row1[0]:
    st.metric("Total Orders", f"{total_orders:,.0f}", f"{pct_delta(total_orders, base_orders):+.1f}% vs network",
               help="Sum of orders for the selected filters and channel view.")
    with st.popover("Breakdown", width="stretch"):
        st.caption("Orders by subregion (current filters)")
        bd = fdf.groupby("Subregion")["ViewOrders"].sum().sort_values(ascending=False).reset_index()
        fig = px.bar(bd, x="Subregion", y="ViewOrders", color_discrete_sequence=[GOLD_LIGHT], text_auto=",.0f")
        st.plotly_chart(style_fig(fig, height=240), width="stretch", key="pop_orders")

# --- 2. Total Revenue ---
with kpi_row1[1]:
    st.metric("Total Revenue", f"${total_revenue:,.0f}", f"{pct_delta(total_revenue, base_revenue):+.1f}% vs network",
               help="Sum of revenue across the active channel view.")
    with st.popover("Breakdown", width="stretch"):
        st.caption("Revenue by channel (current filters)")
        rows = [{"Channel": ch, "Revenue": fdf[CHANNEL_REVENUE_COLS[ch]].sum()} for ch in active_channels]
        bd = pd.DataFrame(rows)
        fig = px.bar(bd, x="Channel", y="Revenue", color="Channel", color_discrete_map=CHANNEL_COLORS, text_auto=",.0f")
        fig.update_layout(showlegend=False)
        st.plotly_chart(style_fig(fig, height=240), width="stretch", key="pop_revenue")

# --- 3. Total Net Profit ---
with kpi_row1[2]:
    st.metric("Total Net Profit", f"${total_profit:,.0f}", f"{pct_delta(total_profit, base_profit):+.1f}% vs network",
               help="Sum of net profit across the active channel view.")
    with st.popover("Breakdown", width="stretch"):
        st.caption("Net profit by channel (current filters)")
        rows = [{"Channel": ch, "Net Profit": fdf[CHANNEL_PROFIT_COLS[ch]].sum()} for ch in active_channels]
        bd = pd.DataFrame(rows)
        fig = px.bar(bd, x="Channel", y="Net Profit", color="Channel", color_discrete_map=CHANNEL_COLORS, text_auto=",.0f")
        fig.update_layout(showlegend=False)
        st.plotly_chart(style_fig(fig, height=240), width="stretch", key="pop_profit")

# --- 4. Profit Margin (gauge) ---
with kpi_row1[3]:
    st.metric("Profit Margin", f"{margin:.1f}%", f"{margin - base_margin:+.1f} pp vs network",
               help="Net profit as a % of revenue for the current filters.")
    with st.popover("Breakdown", width="stretch"):
        st.plotly_chart(
            style_fig(gauge_fig(margin, "Profit Margin", max_val=30,
                                 zones=((0, 8, "#EF4444"), (8, 15, "#F59E0B"), (15, 30, "#10B981"))), height=230),
            width="stretch", key="pop_margin_gauge",
        )

# --- 5. Avg Order Value ---
with kpi_row2[0]:
    st.metric("Avg Order Value", f"${avg_aov:,.2f}", f"{pct_delta(avg_aov, base_aov):+.1f}% vs network",
               help="Mean AOV across restaurants in the current filters.")
    with st.popover("Breakdown", width="stretch"):
        st.caption("Top 5 cuisines by AOV (current filters)")
        bd = fdf.groupby("CuisineType")["AOV"].mean().sort_values(ascending=False).head(5).reset_index()
        fig = px.bar(bd, x="CuisineType", y="AOV", color_discrete_sequence=[GOLD_LIGHT], text_auto=".2f")
        st.plotly_chart(style_fig(fig, height=240), width="stretch", key="pop_aov")

# --- 6. Aggregator Dependence (gauge, lower is better -> inverse delta color) ---
with kpi_row2[1]:
    st.metric("Aggregator Dependence", f"{agg_dep:.1f}%", f"{agg_dep - base_agg_dep:+.1f} pp vs network",
               delta_color="inverse", help="Average combined Uber Eats + DoorDash order share (70%+ = high risk).")
    with st.popover("Breakdown", width="stretch"):
        st.plotly_chart(
            style_fig(gauge_fig(agg_dep, "Aggregator Dependence"), height=230),
            width="stretch", key="pop_aggdep_gauge",
        )

# --- 7. Diversification Score (gauge, higher is better) ---
with kpi_row2[2]:
    st.metric("Diversification Score", f"{div_score:.2f}", f"{div_score - base_div:+.2f} vs network",
               help="Normalized HHI (0-1). Higher = more balanced across all 4 channels.")
    with st.popover("Breakdown", width="stretch"):
        st.plotly_chart(
            style_fig(gauge_fig(div_score * 100, "Diversification", max_val=100,
                                 zones=((0, 60, "#EF4444"), (60, 80, "#F59E0B"), (80, 100, "#10B981")), suffix=""),
                       height=230),
            width="stretch", key="pop_div_gauge",
        )

# --- 8. High-Risk Restaurants ---
with kpi_row2[3]:
    st.metric("High-Risk Restaurants", f"{high_risk_ct:,}", f"{high_risk_ct - base_high_risk_ct:+,} vs network",
               delta_color="inverse", help="Restaurants with >70% combined Uber Eats + DoorDash order dependence.")
    with st.popover("Breakdown", width="stretch"):
        st.caption("Top 5 highest-risk restaurants (current filters)")
        bd = fdf.sort_values("AggregatorDependenceIndex", ascending=False).head(5)[
            ["RestaurantName", "AggregatorDependenceIndex"]
        ].copy()
        bd["AggregatorDependenceIndex"] = (bd["AggregatorDependenceIndex"] * 100).round(1)
        bd.columns = ["Restaurant", "Agg. Dependence (%)"]
        st.dataframe(bd, width="stretch", hide_index=True)

st.markdown("<br>", unsafe_allow_html=True)

# =====================================================================
# TABS — Core Modules
# =====================================================================
tab_exec, tab_channel, tab_geo, tab_cuisine, tab_risk, tab_forecast, tab_explorer = st.tabs(
    [
        "📊 Executive Overview",
        "🧭 Channel Mix Overview",
        "🗺️ Subregion Heatmaps",
        "🍽️ Cuisine vs Channel",
        "🚧 Dependency Risk",
        "🚀 Growth Forecast",
        "🏪 Restaurant Explorer",
    ]
)

# ---------------------------------------------------------------------
# TAB 1 — EXECUTIVE OVERVIEW
# ---------------------------------------------------------------------
with tab_exec:
    c1, c2 = st.columns([1.2, 1])

    with c1:
        st.markdown("#### Revenue vs. Profit by Channel")
        rows = []
        for ch in ["In-Store", "Uber Eats", "DoorDash", "Self-Delivery"]:
            rows.append(
                {
                    "Channel": ch,
                    "Revenue": fdf[CHANNEL_REVENUE_COLS[ch]].sum(),
                    "Net Profit": fdf[CHANNEL_PROFIT_COLS[ch]].sum(),
                }
            )
        rev_profit_df = pd.DataFrame(rows)
        fig = go.Figure()
        fig.add_bar(
            x=rev_profit_df["Channel"], y=rev_profit_df["Revenue"], name="Revenue",
            marker_color=[CHANNEL_COLORS[c] for c in rev_profit_df["Channel"]], opacity=0.55
        )
        fig.add_bar(
            x=rev_profit_df["Channel"], y=rev_profit_df["Net Profit"], name="Net Profit",
            marker_color=[CHANNEL_COLORS[c] for c in rev_profit_df["Channel"]]
        )
        fig.update_layout(barmode="group")
        st.plotly_chart(style_fig(fig), width='stretch')
        st.caption(
            "Aggregator channels generate strong revenue but a disproportionately thinner profit sliver "
            "due to commission costs — a key margin-management signal for stakeholders."
        )

    with c2:
        st.markdown("#### Restaurant Segment Mix")
        seg_counts = fdf["Segment"].value_counts().reset_index()
        seg_counts.columns = ["Segment", "Count"]
        fig = px.pie(
            seg_counts, names="Segment", values="Count", hole=0.5,
            color_discrete_sequence=[GOLD, "#4C6EF5", "#9CA3AF", "#F97316"],
        )
        st.plotly_chart(style_fig(fig, height=420), width='stretch')

    c3, c4 = st.columns(2)
    with c3:
        st.markdown("#### Profit Margin Distribution")
        fig = px.histogram(
            fdf, x="ProfitMargin", nbins=35, color_discrete_sequence=[GOLD_LIGHT],
        )
        fig.update_layout(xaxis_title="Net Profit Margin", yaxis_title="Restaurants")
        fig.update_xaxes(tickformat=".0%")
        st.plotly_chart(style_fig(fig, height=360), width='stretch')

    with c4:
        st.markdown("#### Top 10 Restaurants by Net Profit")
        top10 = fdf.nlargest(10, "ViewProfit")[["RestaurantName", "Subregion", "CuisineType", "ViewProfit"]]
        fig = px.bar(
            top10.sort_values("ViewProfit"),
            x="ViewProfit", y="RestaurantName", orientation="h",
            color="ViewProfit", color_continuous_scale=["#4a3a10", GOLD_LIGHT],
        )
        fig.update_layout(yaxis_title="", xaxis_title="Net Profit ($)", coloraxis_showscale=False)
        st.plotly_chart(style_fig(fig, height=360), width='stretch')

    st.markdown("#### Executive Summary Table")
    exec_summary = pd.DataFrame(
        {
            "Metric": [
                "Total Orders", "Total Revenue", "Total Net Profit", "Overall Margin",
                "Avg Order Value", "Restaurants in View", "In-Store Share", "Delivery Share",
            ],
            "Value": [
                f"{total_orders:,.0f}", f"${total_revenue:,.0f}", f"${total_profit:,.0f}", f"{margin:.2f}%",
                f"${avg_aov:,.2f}", f"{len(fdf):,}",
                f"{fdf['InStoreShare_calc'].mean()*100:.1f}%",
                f"{(fdf['UE_share_total']+fdf['DD_share_total']+fdf['SD_share_total']).mean()*100:.1f}%",
            ],
        }
    )
    st.dataframe(exec_summary, width='stretch', hide_index=True)

# ---------------------------------------------------------------------
# TAB 2 — CHANNEL MIX OVERVIEW
# ---------------------------------------------------------------------
with tab_channel:
    c1, c2 = st.columns([1, 1])

    with c1:
        st.markdown("#### Order Volume by Channel")
        vol = pd.Series({ch: fdf[CHANNEL_ORDER_COLS[ch]].sum() for ch in ["In-Store", "Uber Eats", "DoorDash", "Self-Delivery"]})
        vol_df = pd.DataFrame({"Channel": vol.index, "Orders": vol.values})
        fig = px.bar(
            vol_df,
            x="Channel", y="Orders", color="Channel", color_discrete_map=CHANNEL_COLORS, text_auto=",.0f",
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(style_fig(fig, height=380), width='stretch')

    with c2:
        st.markdown("#### Overall Market Share")
        share = (vol / vol.sum() * 100).round(1)
        fig = px.pie(
            names=share.index, values=share.values, hole=0.45,
            color=share.index, color_discrete_map=CHANNEL_COLORS,
        )
        st.plotly_chart(style_fig(fig, height=380), width='stretch')

    c3, c4 = st.columns(2)
    with c3:
        st.markdown("#### In-Store vs. Delivery Dominance")
        instore_v = fdf["InStoreOrders"].sum()
        delivery_v = fdf["UberEatsOrders"].sum() + fdf["DoorDashOrders"].sum() + fdf["SelfDeliveryOrders"].sum()
        fig = go.Figure(
            go.Bar(
                x=[instore_v, delivery_v], y=["In-Store", "Delivery"], orientation="h",
                marker_color=["#9CA3AF", GOLD_LIGHT], text=[f"{instore_v:,.0f}", f"{delivery_v:,.0f}"],
                textposition="auto",
            )
        )
        st.plotly_chart(style_fig(fig, height=260), width='stretch')
        ratio = delivery_v / instore_v if instore_v else np.nan
        st.info(f"Delivery channels outpace in-store dining by **{ratio:.1f}x** in the current filtered view.", icon="🛵")

    with c4:
        st.markdown("#### Net Profit per Order by Channel")
        rows = []
        for ch in ["In-Store", "Uber Eats", "DoorDash", "Self-Delivery"]:
            o = fdf[CHANNEL_ORDER_COLS[ch]].sum()
            p = fdf[CHANNEL_PROFIT_COLS[ch]].sum()
            rows.append({"Channel": ch, "Profit per Order": p / o if o else 0})
        ppo = pd.DataFrame(rows)
        fig = px.bar(
            ppo, x="Channel", y="Profit per Order", color="Channel", color_discrete_map=CHANNEL_COLORS,
            text_auto=".2f",
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(style_fig(fig, height=260), width='stretch')

    st.markdown("#### Channel Volume Trend by Segment")
    seg_channel = fdf.groupby("Segment")[list(CHANNEL_ORDER_COLS.values())].sum()
    seg_channel.columns = list(CHANNEL_ORDER_COLS.keys())
    fig = px.bar(
        seg_channel.reset_index().melt(id_vars="Segment", var_name="Channel", value_name="Orders"),
        x="Segment", y="Orders", color="Channel", color_discrete_map=CHANNEL_COLORS, barmode="stack",
    )
    st.plotly_chart(style_fig(fig, height=380), width='stretch')

# ---------------------------------------------------------------------
# TAB 3 — SUBREGION HEATMAPS
# ---------------------------------------------------------------------
with tab_geo:
    st.markdown("#### Channel Share (%) by Subregion — Heatmap")
    heat_data = fdf.groupby("Subregion")[list(CHANNEL_ORDER_COLS.values())].sum()
    heat_data.columns = list(CHANNEL_ORDER_COLS.keys())
    heat_pct = heat_data.div(heat_data.sum(axis=1), axis=0) * 100

    fig = px.imshow(
        heat_pct.values,
        x=heat_pct.columns, y=heat_pct.index,
        color_continuous_scale=[[0, "#141414"], [0.5, "#5c481a"], [1, GOLD_LIGHT]],
        text_auto=".1f", aspect="auto",
    )
    fig.update_layout(coloraxis_colorbar=dict(title="Share %"))
    st.plotly_chart(style_fig(fig, height=340), width='stretch')

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Orders by Subregion")
        subreg_orders = fdf.groupby("Subregion")["ViewOrders"].sum().sort_values(ascending=False)
        fig = px.bar(
            subreg_orders.reset_index(), x="Subregion", y="ViewOrders",
            color="ViewOrders", color_continuous_scale=["#4a3a10", GOLD_LIGHT], text_auto=",.0f",
        )
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(style_fig(fig, height=360), width='stretch')

    with c2:
        st.markdown("#### Revenue & Profit by Subregion")
        subreg_fin = fdf.groupby("Subregion")[["ViewRevenue", "ViewProfit"]].sum().reset_index()
        fig = px.bar(
            subreg_fin.melt(id_vars="Subregion", var_name="Metric", value_name="Amount"),
            x="Subregion", y="Amount", color="Metric", barmode="group",
            color_discrete_map={"ViewRevenue": "#4C6EF5", "ViewProfit": GOLD_LIGHT},
        )
        st.plotly_chart(style_fig(fig, height=360), width='stretch')

    st.markdown("#### Urban vs. Suburban Ordering Behaviour")
    urban_note = heat_pct[["Uber Eats", "DoorDash"]].sum(axis=1).sort_values(ascending=False)
    for reg, val in urban_note.items():
        bar_color = "#EF4444" if val > 65 else ("#F59E0B" if val > 50 else "#10B981")
        st.markdown(
            f"<div style='display:flex;align-items:center;gap:10px;margin-bottom:6px;'>"
            f"<div style='width:130px;'>{reg}</div>"
            f"<div style='background:{bar_color};width:{val*3:.0f}px;max-width:400px;height:14px;border-radius:6px;'></div>"
            f"<div>{val:.1f}% aggregator-delivered</div></div>",
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------------------
# TAB 4 — CUISINE VS CHANNEL
# ---------------------------------------------------------------------
with tab_cuisine:
    st.markdown("#### Channel Mix by Cuisine Type")
    cui_data = fdf.groupby("CuisineType")[list(CHANNEL_ORDER_COLS.values())].sum()
    cui_data.columns = list(CHANNEL_ORDER_COLS.keys())
    cui_pct = cui_data.div(cui_data.sum(axis=1), axis=0) * 100
    cui_pct = cui_pct.loc[cui_pct.sum(axis=1).sort_values(ascending=False).index]

    fig = px.bar(
        cui_pct.reset_index().melt(id_vars="CuisineType", var_name="Channel", value_name="Share %"),
        x="Share %", y="CuisineType", color="Channel", orientation="h",
        color_discrete_map=CHANNEL_COLORS, barmode="stack",
    )
    st.plotly_chart(style_fig(fig, height=420), width='stretch')

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Most Aggregator-Dependent Cuisines")
        agg_by_cuisine = (cui_pct["Uber Eats"] + cui_pct["DoorDash"]).sort_values(ascending=False)
        agg_by_cuisine_df = pd.DataFrame({"CuisineType": agg_by_cuisine.index, "Aggregator %": agg_by_cuisine.values})
        fig = px.bar(
            agg_by_cuisine_df,
            x="CuisineType", y="Aggregator %", color="Aggregator %",
            color_continuous_scale=["#4a3a10", "#EF4444"], text_auto=".1f",
        )
        fig.update_layout(yaxis_title="Aggregator Share (%)", xaxis_title="", coloraxis_showscale=False)
        st.plotly_chart(style_fig(fig, height=360), width='stretch')

    with c2:
        st.markdown("#### Channel Mix by Segment")
        seg_data = fdf.groupby("Segment")[list(CHANNEL_ORDER_COLS.values())].sum()
        seg_data.columns = list(CHANNEL_ORDER_COLS.keys())
        seg_pct = seg_data.div(seg_data.sum(axis=1), axis=0) * 100
        fig = px.bar(
            seg_pct.reset_index().melt(id_vars="Segment", var_name="Channel", value_name="Share %"),
            x="Segment", y="Share %", color="Channel", color_discrete_map=CHANNEL_COLORS, barmode="stack",
        )
        st.plotly_chart(style_fig(fig, height=360), width='stretch')

    st.markdown("#### Average Order Value by Cuisine")
    aov_cuisine = fdf.groupby("CuisineType")["AOV"].mean().sort_values(ascending=False)
    fig = px.bar(
        aov_cuisine.reset_index(), x="CuisineType", y="AOV", color="AOV",
        color_continuous_scale=["#1a1a1a", GOLD_LIGHT], text_auto=".2f",
    )
    fig.update_layout(coloraxis_showscale=False)
    st.plotly_chart(style_fig(fig, height=340), width='stretch')

# ---------------------------------------------------------------------
# TAB 5 — DEPENDENCY RISK
# ---------------------------------------------------------------------
with tab_risk:
    c1, c2 = st.columns([1, 1.3])

    with c1:
        st.markdown("#### Channel-Risk Profile")
        risk_bins = pd.cut(
            fdf["AggregatorDependenceIndex"], bins=[0, 0.5, 0.7, 1.0],
            labels=["Balanced (<50%)", "Moderate (50-70%)", "High Risk (>70%)"],
        )
        risk_counts = risk_bins.value_counts().reindex(
            ["Balanced (<50%)", "Moderate (50-70%)", "High Risk (>70%)"]
        )
        risk_counts_df = pd.DataFrame({"Risk Band": risk_counts.index.astype(str), "Restaurants": risk_counts.values})
        fig = px.bar(
            risk_counts_df, x="Risk Band", y="Restaurants",
            color="Risk Band", color_discrete_map={
                "Balanced (<50%)": "#10B981", "Moderate (50-70%)": "#F59E0B", "High Risk (>70%)": "#EF4444"
            }, text_auto=True,
        )
        fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Restaurants")
        st.plotly_chart(style_fig(fig, height=340), width='stretch')

        st.metric("Restaurants with >70% single-aggregator share", f"{(fdf[['UE_share_total','DD_share_total']].max(axis=1) > 0.70).sum():,}")
        st.metric("Restaurants with >70% combined aggregator dependence", f"{(fdf['AggregatorDependenceIndex'] > 0.70).sum():,}")

    with c2:
        st.markdown("#### Diversification Score Distribution")
        fig = px.histogram(fdf, x="DiversificationScore", nbins=30, color_discrete_sequence=[GOLD_LIGHT])
        fig.add_vline(x=fdf["DiversificationScore"].median(), line_dash="dash", line_color="#EF4444")
        fig.update_layout(xaxis_title="Diversification Score (1 = fully balanced)", yaxis_title="Restaurants")
        st.plotly_chart(style_fig(fig, height=340), width='stretch')

    st.markdown("#### Risk Scatter: Aggregator Dependence vs. Profit Margin")
    fig = px.scatter(
        fdf, x="AggregatorDependenceIndex", y="ProfitMargin", color="Segment",
        size="MonthlyOrders", hover_data=["RestaurantName", "Subregion", "CuisineType"],
        color_discrete_sequence=[GOLD, "#4C6EF5", "#9CA3AF", "#F97316"],
    )
    fig.update_xaxes(tickformat=".0%", title="Aggregator Dependence Index")
    fig.update_yaxes(tickformat=".0%", title="Profit Margin")
    fig.add_vline(x=0.70, line_dash="dash", line_color="#EF4444", annotation_text="70% risk threshold")
    st.plotly_chart(style_fig(fig, height=420), width='stretch')

    st.markdown("#### Top 15 Highest-Risk Restaurants")
    risk_table = fdf.sort_values("AggregatorDependenceIndex", ascending=False).head(15)[
        ["RestaurantName", "CuisineType", "Segment", "Subregion", "AggregatorDependenceIndex", "DiversificationScore", "ProfitMargin"]
    ].copy()
    risk_table["AggregatorDependenceIndex"] = (risk_table["AggregatorDependenceIndex"] * 100).round(1)
    risk_table["ProfitMargin"] = (risk_table["ProfitMargin"] * 100).round(1)
    risk_table["DiversificationScore"] = risk_table["DiversificationScore"].round(2)
    risk_table.columns = ["Restaurant", "Cuisine", "Segment", "Subregion", "Agg. Dependence (%)", "Diversification Score", "Profit Margin (%)"]
    st.dataframe(risk_table, width='stretch', hide_index=True)

# ---------------------------------------------------------------------
# TAB 6 — GROWTH FORECAST (bonus predictive module)
# ---------------------------------------------------------------------
with tab_forecast:
    st.markdown(
        "#### Demand & Profit Forecast — Compound Growth Projection\n"
        "Each restaurant's own `GrowthFactor` (month-over-month multiplier) is compounded forward to "
        "project network performance."
    )
    horizon = st.slider("Forecast horizon (months)", 1, 24, 6)

    proj_orders = (fdf["MonthlyOrders"] * (fdf["GrowthFactor"] ** horizon)).sum()
    proj_revenue = (fdf["TotalRevenue"] * (fdf["GrowthFactor"] ** horizon)).sum()
    proj_profit = (fdf["TotalNetProfit"] * (fdf["GrowthFactor"] ** horizon)).sum()

    f1, f2, f3 = st.columns(3)
    f1.metric(f"Projected Orders (+{horizon}mo)", f"{proj_orders:,.0f}", f"{(proj_orders/fdf['MonthlyOrders'].sum()-1)*100:+.1f}%")
    f2.metric(f"Projected Revenue (+{horizon}mo)", f"${proj_revenue:,.0f}", f"{(proj_revenue/fdf['TotalRevenue'].sum()-1)*100:+.1f}%")
    f3.metric(f"Projected Net Profit (+{horizon}mo)", f"${proj_profit:,.0f}", f"{(proj_profit/fdf['TotalNetProfit'].sum()-1)*100:+.1f}%")

    months = list(range(0, horizon + 1))
    traj = pd.DataFrame(
        {
            "Month": months,
            "Orders": [(fdf["MonthlyOrders"] * (fdf["GrowthFactor"] ** m)).sum() for m in months],
            "Revenue": [(fdf["TotalRevenue"] * (fdf["GrowthFactor"] ** m)).sum() for m in months],
            "Net Profit": [(fdf["TotalNetProfit"] * (fdf["GrowthFactor"] ** m)).sum() for m in months],
        }
    )
    c1, c2 = st.columns(2)
    with c1:
        fig = px.area(traj, x="Month", y="Orders", color_discrete_sequence=[GOLD_LIGHT])
        fig.update_layout(title="Projected Order Volume")
        st.plotly_chart(style_fig(fig, height=340), width='stretch')
    with c2:
        fig = px.line(traj, x="Month", y=["Revenue", "Net Profit"], color_discrete_sequence=["#4C6EF5", GOLD_LIGHT])
        fig.update_layout(title="Projected Revenue vs. Net Profit")
        st.plotly_chart(style_fig(fig, height=340), width='stretch')

    st.markdown("#### Channel-Level Growth Outlook")
    rows = []
    for ch in ["In-Store", "Uber Eats", "DoorDash", "Self-Delivery"]:
        cur = fdf[CHANNEL_ORDER_COLS[ch]].sum()
        fut = (fdf[CHANNEL_ORDER_COLS[ch]] * (fdf["GrowthFactor"] ** horizon)).sum()
        rows.append({"Channel": ch, "Current Orders": cur, f"+{horizon}mo Projected": fut, "Growth %": (fut/cur-1)*100 if cur else 0})
    ch_growth = pd.DataFrame(rows)
    fig = px.bar(
        ch_growth.melt(id_vars="Channel", value_vars=["Current Orders", f"+{horizon}mo Projected"], var_name="Period", value_name="Orders"),
        x="Channel", y="Orders", color="Period", barmode="group",
        color_discrete_sequence=["#5A5A5A", GOLD_LIGHT],
    )
    st.plotly_chart(style_fig(fig, height=360), width='stretch')
    st.dataframe(ch_growth.style.format({"Current Orders": "{:,.0f}", f"+{horizon}mo Projected": "{:,.0f}", "Growth %": "{:+.1f}%"}), width='stretch', hide_index=True)

    declining_ct = (fdf["GrowthFactor"] < 1.0).sum()
    growing_ct = (fdf["GrowthFactor"] > 1.0).sum()
    st.info(
        f"📉 **{declining_ct:,}** restaurants in view show a declining GrowthFactor (<1.0), while "
        f"📈 **{growing_ct:,}** are trending upward. Use this to prioritize retention efforts.",
        icon="📊",
    )

# ---------------------------------------------------------------------
# TAB 7 — RESTAURANT EXPLORER (drill-down from summary KPIs to individual records)
# ---------------------------------------------------------------------
with tab_explorer:
    st.markdown(
        "#### Drill Down: Summary KPIs → Individual Restaurant Records\n"
        "This dataset's finest available granularity is the individual restaurant branch "
        "(no line-item transaction feed is provided). Search or sort below to drill from any "
        "network-level KPI down to a single restaurant, then select it for a full channel breakdown — "
        "the equivalent of a transaction-level drill-down for this dataset."
    )

    search = st.text_input("🔎 Search restaurant by name", "")
    explorer_df = fdf.copy()
    if search:
        explorer_df = explorer_df[explorer_df["RestaurantName"].str.contains(search, case=False, na=False)]

    # Restaurant Lifetime Value analogue: 12-month cumulative projected net profit
    g = explorer_df["GrowthFactor"]
    months = 12
    cum_factor = np.where(np.isclose(g, 1.0), months, (1 - g ** months) / (1 - g))
    explorer_df["ProjectedValue12mo"] = explorer_df["TotalNetProfit"] * cum_factor

    display_cols = [
        "RestaurantID", "RestaurantName", "CuisineType", "Segment", "Subregion",
        "MonthlyOrders", "TotalRevenue", "TotalNetProfit", "ProfitMargin",
        "AggregatorDependenceIndex", "DiversificationScore", "ProjectedValue12mo",
    ]
    table = explorer_df[display_cols].sort_values("TotalNetProfit", ascending=False).copy()
    table["ProfitMargin"] = (table["ProfitMargin"] * 100).round(1)
    table["AggregatorDependenceIndex"] = (table["AggregatorDependenceIndex"] * 100).round(1)
    table["DiversificationScore"] = table["DiversificationScore"].round(2)
    table.columns = [
        "ID", "Restaurant", "Cuisine", "Segment", "Subregion", "Monthly Orders", "Revenue ($)",
        "Net Profit ($)", "Margin (%)", "Agg. Dependence (%)", "Diversification", "Projected 12-mo Value ($)",
    ]

    st.caption(f"Showing {len(table):,} of {len(fdf):,} restaurants in the current filtered view")
    st.dataframe(
        table,
        width="stretch",
        hide_index=True,
        height=340,
        column_config={
            "Revenue ($)": st.column_config.NumberColumn(format="$%.0f"),
            "Net Profit ($)": st.column_config.NumberColumn(format="$%.0f"),
            "Projected 12-mo Value ($)": st.column_config.NumberColumn(format="$%.0f"),
            "Margin (%)": st.column_config.ProgressColumn(min_value=-20, max_value=30, format="%.1f%%"),
            "Agg. Dependence (%)": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%.1f%%"),
        },
    )

    st.markdown("#### Single-Restaurant Drill-Down")
    options = sorted(explorer_df["RestaurantName"].unique())
    if options:
        chosen = st.selectbox("Select a restaurant for its individual channel breakdown", options)
        r = explorer_df[explorer_df["RestaurantName"] == chosen].iloc[0]

        rc1, rc2, rc3, rc4 = st.columns(4)
        rc1.metric("Monthly Orders", f"{r['MonthlyOrders']:,.0f}")
        rc2.metric("Revenue", f"${r['TotalRevenue']:,.0f}")
        rc3.metric("Net Profit", f"${r['TotalNetProfit']:,.0f}")
        rc4.metric("Projected 12-mo Value", f"${r['ProjectedValue12mo']:,.0f}")

        rr1, rr2 = st.columns(2)
        with rr1:
            rows = [
                {"Channel": ch, "Orders": r[CHANNEL_ORDER_COLS[ch]], "Revenue": r[CHANNEL_REVENUE_COLS[ch]], "Net Profit": r[CHANNEL_PROFIT_COLS[ch]]}
                for ch in ["In-Store", "Uber Eats", "DoorDash", "Self-Delivery"]
            ]
            rdf = pd.DataFrame(rows)
            fig = px.bar(rdf, x="Channel", y="Orders", color="Channel", color_discrete_map=CHANNEL_COLORS, text_auto=",.0f")
            fig.update_layout(showlegend=False, title="Orders by Channel — This Restaurant")
            st.plotly_chart(style_fig(fig, height=320), width="stretch")
        with rr2:
            fig = px.bar(rdf, x="Channel", y=["Revenue", "Net Profit"], barmode="group",
                         color_discrete_sequence=["#4C6EF5", GOLD_LIGHT])
            fig.update_layout(title="Revenue vs. Net Profit — This Restaurant")
            st.plotly_chart(style_fig(fig, height=320), width="stretch")

        st.caption(
            f"**{chosen}** · {r['CuisineType']} · {r['Segment']} · {r['Subregion']} · "
            f"Aggregator dependence: {r['AggregatorDependenceIndex']*100:.1f}% · "
            f"GrowthFactor: {r['GrowthFactor']:.3f}"
        )
    else:
        st.info("No restaurants match your search.")

# =====================================================================
# FOOTER
# =====================================================================
st.markdown(f"""
<div style="text-align: center; margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid rgba(140, 135, 175, 0.22); font-size: 12px; font-weight: 700; line-height: 1.5;">
        SkyCity Auckland Restaurants & Bars — Order Channel Performance and Market Share Analytics <span style="color: #9990CC; font-weight: 600; font-size: 12px;"></span><br>
        Prepared by <span style="color: #55FF06; font-weight: 600; font-size: 12px; letter-spacing: 0.6px;">M SANDEEP REDDY</span>
</div>
""", unsafe_allow_html=True)