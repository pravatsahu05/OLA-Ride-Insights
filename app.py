"""
=============================================================================
OLA RIDE INSIGHTS - NEXT-GEN ENTERPRISE MOBILITY BI PLATFORM
Domain: Ride-Sharing & Mobility Analytics
Technologies: Python, Streamlit, SQLite, Plotly, Pandas, NumPy
=============================================================================
"""

import os
import sqlite3
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import streamlit as st

from src.db_manager import PREDEFINED_SQL_QUERIES, execute_query, get_connection

# -----------------------------------------------------------------------------
# 1. STREAMLIT CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="OLA Mobility OS | Executive BI & Telemetry",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------------------
# 2. ULTRA-MODERN LUXURY MOBILITY CSS THEME
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    :root {
        --ola-lime: #B2FF00;
        --ola-lime-dark: #84CC00;
        --ola-lime-glow: rgba(178, 255, 0, 0.25);
        --bg-obsidian: #080B11;
        --card-bg: rgba(15, 23, 42, 0.7);
        --card-border: rgba(255, 255, 255, 0.08);
        --text-primary: #F8FAFC;
        --text-secondary: #94A3B8;
        --text-muted: #64748B;
        --accent-emerald: #10B981;
        --accent-rose: #F43F5E;
        --accent-amber: #F59E0B;
        --accent-cyan: #06B6D4;
        --accent-violet: #8B5CF6;
    }

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text-primary);
    }
    
    /* Smooth dark background for container */
    .stApp {
        background: radial-gradient(circle at 15% 15%, rgba(18, 28, 48, 0.5) 0%, #080B11 90%);
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #080B11;
    }
    ::-webkit-scrollbar-thumb {
        background: #1E293B;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--ola-lime);
    }

    /* Hero Banner */
    .hero-container {
        position: relative;
        background: linear-gradient(135deg, rgba(17, 24, 39, 0.85) 0%, rgba(15, 23, 42, 0.6) 100%);
        border: 1px solid var(--card-border);
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 24px;
        box-shadow: 0 16px 36px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        overflow: hidden;
    }
    .hero-container::before {
        content: "";
        position: absolute;
        top: -60px;
        right: -60px;
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, var(--ola-lime-glow) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
    }
    
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(178, 255, 0, 0.12);
        border: 1px solid rgba(178, 255, 0, 0.3);
        color: var(--ola-lime);
        font-size: 0.75rem;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 12px;
    }
    
    .pulse-dot {
        width: 8px;
        height: 8px;
        background-color: var(--ola-lime);
        border-radius: 50%;
        box-shadow: 0 0 10px var(--ola-lime);
        animation: pulse 1.8s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(0.9); opacity: 0.8; }
        50% { transform: scale(1.3); opacity: 1; }
        100% { transform: scale(0.9); opacity: 0.8; }
    }

    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.2;
        margin: 0 0 8px 0;
        background: linear-gradient(180deg, #FFFFFF 0%, #94A3B8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-title span {
        color: var(--ola-lime);
        -webkit-text-fill-color: var(--ola-lime);
    }
    
    .hero-subtitle {
        color: var(--text-secondary);
        font-size: 0.95rem;
        line-height: 1.6;
        margin: 0;
        max-width: 920px;
    }

    /* Meta Badges Ribbon */
    .meta-ribbon {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 18px;
    }
    .meta-pill {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 5px 12px;
        font-size: 0.8rem;
        color: #CBD5E1;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Next-Gen KPI Metric Cards */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 16px;
        margin-bottom: 24px;
    }
    .modern-kpi-card {
        background: linear-gradient(145deg, rgba(23, 32, 54, 0.8) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid var(--card-border);
        border-radius: 14px;
        padding: 18px 20px;
        position: relative;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
    }
    .modern-kpi-card:hover {
        transform: translateY(-4px);
        border-color: rgba(178, 255, 0, 0.4);
        box-shadow: 0 14px 28px rgba(0, 0, 0, 0.4), 0 0 16px var(--ola-lime-glow);
    }
    .kpi-top-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }
    .kpi-label {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        color: var(--text-secondary);
    }
    .kpi-icon-box {
        width: 34px;
        height: 34px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
    }
    .icon-lime { background: rgba(178, 255, 0, 0.15); color: var(--ola-lime); border: 1px solid rgba(178, 255, 0, 0.25); }
    .icon-emerald { background: rgba(16, 185, 129, 0.15); color: var(--accent-emerald); border: 1px solid rgba(16, 185, 129, 0.25); }
    .icon-cyan { background: rgba(6, 182, 212, 0.15); color: var(--accent-cyan); border: 1px solid rgba(6, 182, 212, 0.25); }
    .icon-rose { background: rgba(244, 63, 94, 0.15); color: var(--accent-rose); border: 1px solid rgba(244, 63, 94, 0.25); }
    .icon-amber { background: rgba(245, 158, 11, 0.15); color: var(--accent-amber); border: 1px solid rgba(245, 158, 11, 0.25); }
    .icon-violet { background: rgba(139, 92, 246, 0.15); color: var(--accent-violet); border: 1px solid rgba(139, 92, 246, 0.25); }

    .kpi-value-text {
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #FFFFFF;
        line-height: 1;
        margin-bottom: 8px;
    }
    .kpi-sub-row {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 0.8rem;
        color: var(--text-muted);
    }

    /* Progress bar in card */
    .kpi-bar-container {
        width: 100%;
        height: 4px;
        background: rgba(255, 255, 255, 0.08);
        border-radius: 3px;
        margin-top: 10px;
        overflow: hidden;
    }
    .kpi-bar-fill {
        height: 100%;
        border-radius: 3px;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(15, 23, 42, 0.6);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid var(--card-border);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        padding: 10px 22px !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        color: var(--text-secondary) !important;
        border: none !important;
        background: transparent !important;
        transition: all 0.2s ease !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(178, 255, 0, 0.2) 0%, rgba(132, 204, 0, 0.15) 100%) !important;
        color: var(--ola-lime) !important;
        border: 1px solid rgba(178, 255, 0, 0.3) !important;
        box-shadow: 0 4px 12px rgba(178, 255, 0, 0.15) !important;
    }

    /* Chart Container Card */
    .chart-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid var(--card-border);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.2);
    }
    .chart-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .chart-desc {
        font-size: 0.8rem;
        color: var(--text-secondary);
        margin-bottom: 12px;
    }

    /* SQL Terminal Box */
    .sql-terminal {
        background: #05080E;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 4px solid var(--ola-lime);
        border-radius: 10px;
        padding: 16px 20px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.88rem;
        color: #E2E8F0;
        margin: 12px 0 16px 0;
        box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.6);
    }
    
    /* Strategy & Insight Cards */
    .strategy-card {
        background: linear-gradient(145deg, rgba(23, 32, 54, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid var(--card-border);
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 18px;
        transition: transform 0.2s ease;
    }
    .strategy-card:hover {
        transform: translateY(-2px);
    }
    .strategy-pill {
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 800;
        text-transform: uppercase;
        padding: 3px 10px;
        border-radius: 12px;
        margin-bottom: 10px;
        letter-spacing: 0.6px;
    }

    /* Hide sidebar as filters are moved to the top */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Top Filter Console Deck */
    .top-filter-card {
        background: linear-gradient(145deg, rgba(23, 32, 54, 0.7) 0%, rgba(15, 23, 42, 0.85) 100%);
        border: 1px solid var(--card-border);
        border-radius: 14px;
        padding: 16px 20px 10px 20px;
        margin-bottom: 22px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(12px);
    }
    .filter-header-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        padding-bottom: 10px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    }
    .filter-title {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.88rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        color: #FFFFFF;
    }
    .filter-count-badge {
        background: rgba(178, 255, 0, 0.12);
        color: var(--ola-lime);
        border: 1px solid rgba(178, 255, 0, 0.25);
        font-size: 0.75rem;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 3. FAST CACHED DATA PIPELINE
# -----------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def get_master_data():
    csv_path = "data/ola_rides_cleaned.csv" if os.path.exists("data/ola_rides_cleaned.csv") else "ola_rides_cleaned.csv"
    if not os.path.exists(csv_path):
        if os.path.exists("ola_rides.csv"):
            csv_path = "ola_rides.csv"
        else:
            raise FileNotFoundError("Cleaned dataset not found.")
            
    df = pd.read_csv(csv_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Ride_Date'] = pd.to_datetime(df['Ride_Date']).dt.date
    return df

try:
    master_df = get_master_data()
except Exception as e:
    st.error(f"Failed to load dataset: {e}")
    st.stop()


# -----------------------------------------------------------------------------
# 4. PLOTLY UNIFIED DARK LUXURY THEME
# -----------------------------------------------------------------------------
def apply_chart_style(fig, height=380):
    fig.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=15, r=15, t=35, b=15),
        font=dict(family="Plus Jakarta Sans", size=12, color="#94A3B8"),
        hoverlabel=dict(
            bgcolor="#0F172A",
            bordercolor="rgba(178, 255, 0, 0.4)",
            font=dict(family="Plus Jakarta Sans", size=12, color="#FFFFFF")
        ),
        xaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.05)",
            linecolor="rgba(255, 255, 255, 0.08)",
            tickfont=dict(color="#94A3B8")
        ),
        yaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.05)",
            linecolor="rgba(255, 255, 255, 0.08)",
            tickfont=dict(color="#94A3B8")
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11, color="#CBD5E1")
        )
    )
    return fig


# -----------------------------------------------------------------------------
# 5. HERO HEADER BANNER
# -----------------------------------------------------------------------------
st.markdown("""
<div class="hero-container">
    <div class="status-badge">
        <span class="pulse-dot"></span>
        ENTERPRISE MOBILITY TELEMETRY & BUSINESS INTELLIGENCE
    </div>
    <h1 class="hero-title">
        OLA Ride <span>Insights</span> Control Center
    </h1>
    <p class="hero-subtitle">
        Unified analytics platform analyzing 103,024 ride requests across Bengaluru. Uncovering peak demand windows, 
        optimizing fleet distribution, deconstructing customer and driver cancellation friction, and benchmarking revenue pipelines.
    </p>
    <div class="meta-ribbon">
        <div class="meta-pill">📍 <b>Metro Cluster:</b> Bengaluru Urban (50 Hubs)</div>
        <div class="meta-pill">📅 <b>Timeline:</b> July 01 - July 31, 2024</div>
        <div class="meta-pill">🏎️ <b>Vehicle Tiers:</b> 7 Categories</div>
        <div class="meta-pill">⚡ <b>Status:</b> Live In-Memory Telemetry</div>
    </div>
</div>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 6. TOP FILTER CONSOLE DECK (HORIZONTAL FILTERS)
# -----------------------------------------------------------------------------
st.markdown("""
<div class="top-filter-card">
    <div class="filter-header-row">
        <div class="filter-title">
            <span>🎛️</span> Global Telemetry Filter Deck
        </div>
        <span class="filter-count-badge">Active Scope: Bengaluru Metro</span>
    </div>
</div>
""", unsafe_allow_html=True)

f_col1, f_col2, f_col3, f_col4 = st.columns([3, 3, 3, 3])

min_date = master_df['Ride_Date'].min()
max_date = master_df['Ride_Date'].max()
all_vehicles = sorted(master_df['Vehicle_Type'].dropna().unique().tolist())
all_statuses = sorted(master_df['Booking_Status'].dropna().unique().tolist())
payment_options = sorted(master_df['Payment_Method'].dropna().unique().tolist())

with f_col1:
    selected_dates = st.date_input(
        "📅 Date Window",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        help="Filter analytics across any custom date range in July 2024"
    )

with f_col2:
    selected_vehicles = st.multiselect(
        "🚗 Fleet Categories",
        options=all_vehicles,
        default=all_vehicles,
        help="Select one or multiple vehicle types"
    )

with f_col3:
    selected_statuses = st.multiselect(
        "🎯 Trip Status",
        options=all_statuses,
        default=all_statuses,
        help="Filter by Success, Canceled, or Driver Not Found"
    )

with f_col4:
    selected_payments = st.multiselect(
        "💳 Payment Gateways",
        options=payment_options,
        default=payment_options,
        help="Filter by payment method for completed trips"
    )

# Quick Fleet Category Tags Ribbon
st.markdown("""
<div style="display: flex; align-items: center; gap: 8px; margin-top: -6px; margin-bottom: 22px; flex-wrap: wrap;">
    <span style="font-size: 0.72rem; color: #64748B; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">Active Fleet Classes:</span>
    <span style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.06); font-size: 0.72rem; padding: 2px 8px; border-radius: 6px; color: #E2E8F0;">🛺 Auto</span>
    <span style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.06); font-size: 0.72rem; padding: 2px 8px; border-radius: 6px; color: #E2E8F0;">🏍️ Bike</span>
    <span style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.06); font-size: 0.72rem; padding: 2px 8px; border-radius: 6px; color: #E2E8F0;">⚡ eBike</span>
    <span style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.06); font-size: 0.72rem; padding: 2px 8px; border-radius: 6px; color: #E2E8F0;">🚗 Mini</span>
    <span style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.06); font-size: 0.72rem; padding: 2px 8px; border-radius: 6px; color: #E2E8F0;">🚘 Prime Sedan</span>
    <span style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.06); font-size: 0.72rem; padding: 2px 8px; border-radius: 6px; color: #E2E8F0;">🚙 Prime SUV</span>
    <span style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.06); font-size: 0.72rem; padding: 2px 8px; border-radius: 6px; color: #E2E8F0;">✨ Prime Plus</span>
</div>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 7. FILTER APPLICATION
# -----------------------------------------------------------------------------
filtered_df = master_df.copy()

if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
    s_date, e_date = selected_dates
    filtered_df = filtered_df[(filtered_df['Ride_Date'] >= s_date) & (filtered_df['Ride_Date'] <= e_date)]
elif isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 1:
    filtered_df = filtered_df[filtered_df['Ride_Date'] == selected_dates[0]]

if selected_vehicles:
    filtered_df = filtered_df[filtered_df['Vehicle_Type'].isin(selected_vehicles)]

if selected_statuses:
    filtered_df = filtered_df[filtered_df['Booking_Status'].isin(selected_statuses)]

if selected_payments and len(selected_payments) < len(payment_options):
    filtered_df = filtered_df[filtered_df['Payment_Method'].isin(selected_payments) | filtered_df['Payment_Method'].isna()]


# -----------------------------------------------------------------------------
# 8. TOP-TIER EXECUTIVE KPI CARDS
# -----------------------------------------------------------------------------
total_count = len(filtered_df)
success_records = filtered_df[filtered_df['Booking_Status'] == 'Success']
successful_count = len(success_records)
success_pct = (successful_count / total_count * 100) if total_count > 0 else 0.0

total_gross_rev = success_records['Booking_Value'].sum()
avg_ride_fare = success_records['Booking_Value'].mean() if successful_count > 0 else 0.0
avg_ride_dist = success_records['Ride_Distance'].mean() if successful_count > 0 else 0.0

cust_cancels = len(filtered_df[filtered_df['Booking_Status'] == 'Canceled by Customer'])
driver_cancels = len(filtered_df[filtered_df['Booking_Status'] == 'Canceled by Driver'])
driver_not_found = len(filtered_df[filtered_df['Booking_Status'] == 'Driver Not Found'])
total_cancels = cust_cancels + driver_cancels
cancellation_pct = (total_cancels / total_count * 100) if total_count > 0 else 0.0

avg_c_rating = success_records['Customer_Rating'].dropna().mean() if successful_count > 0 else 0.0
avg_d_rating = success_records['Driver_Ratings'].dropna().mean() if successful_count > 0 else 0.0

st.markdown(f"""
<div class="kpi-grid">
    <!-- Card 1: Total Bookings -->
    <div class="modern-kpi-card">
        <div class="kpi-top-row">
            <span class="kpi-label">Total Demand</span>
            <div class="kpi-icon-box icon-lime">📊</div>
        </div>
        <div class="kpi-value-text">{total_count:,}</div>
        <div class="kpi-sub-row">
            <span>Across 50 Locations</span>
        </div>
        <div class="kpi-bar-container">
            <div class="kpi-bar-fill" style="width: 100%; background: var(--ola-lime);"></div>
        </div>
    </div>

    <!-- Card 2: Success Rate -->
    <div class="modern-kpi-card">
        <div class="kpi-top-row">
            <span class="kpi-label">Fulfillment Rate</span>
            <div class="kpi-icon-box icon-emerald">🎯</div>
        </div>
        <div class="kpi-value-text" style="color: #4ADE80;">{success_pct:.1f}%</div>
        <div class="kpi-sub-row">
            <span style="color: #4ADE80; font-weight: 700;">{successful_count:,}</span> completed
        </div>
        <div class="kpi-bar-container">
            <div class="kpi-bar-fill" style="width: {min(success_pct, 100)}%; background: #4ADE80;"></div>
        </div>
    </div>

    <!-- Card 3: Revenue -->
    <div class="modern-kpi-card">
        <div class="kpi-top-row">
            <span class="kpi-label">Gross Revenue</span>
            <div class="kpi-icon-box icon-cyan">💰</div>
        </div>
        <div class="kpi-value-text">₹{total_gross_rev/1e6:.2f}M</div>
        <div class="kpi-sub-row">
            <span>Avg Fare: <b>₹{avg_ride_fare:.1f}</b></span>
        </div>
        <div class="kpi-bar-container">
            <div class="kpi-bar-fill" style="width: 85%; background: #06B6D4;"></div>
        </div>
    </div>

    <!-- Card 4: Distance -->
    <div class="modern-kpi-card">
        <div class="kpi-top-row">
            <span class="kpi-label">Avg Distance</span>
            <div class="kpi-icon-box icon-violet">📍</div>
        </div>
        <div class="kpi-value-text">{avg_ride_dist:.1f} <span style="font-size: 1rem; color: #94A3B8;">km</span></div>
        <div class="kpi-sub-row">
            <span>Citywide Fleet Mean</span>
        </div>
        <div class="kpi-bar-container">
            <div class="kpi-bar-fill" style="width: 70%; background: #8B5CF6;"></div>
        </div>
    </div>

    <!-- Card 5: Cancellations -->
    <div class="modern-kpi-card">
        <div class="kpi-top-row">
            <span class="kpi-label">Cancellation Rate</span>
            <div class="kpi-icon-box icon-rose">⚠️</div>
        </div>
        <div class="kpi-value-text" style="color: #F87171;">{cancellation_pct:.1f}%</div>
        <div class="kpi-sub-row">
            <span style="color: #F87171; font-weight: 700;">{total_cancels:,}</span> cancelled
        </div>
        <div class="kpi-bar-container">
            <div class="kpi-bar-fill" style="width: {min(cancellation_pct, 100)}%; background: #F87171;"></div>
        </div>
    </div>

    <!-- Card 6: Ratings -->
    <div class="modern-kpi-card">
        <div class="kpi-top-row">
            <span class="kpi-label">Quality Score</span>
            <div class="kpi-icon-box icon-amber">⭐</div>
        </div>
        <div class="kpi-value-text">{avg_c_rating:.2f} <span style="font-size: 1rem; color: #94A3B8;">/ 5</span></div>
        <div class="kpi-sub-row">
            <span>Driver Score: <b>{avg_d_rating:.2f}</b></span>
        </div>
        <div class="kpi-bar-container">
            <div class="kpi-bar-fill" style="width: {(avg_c_rating/5)*100:.1f}%; background: #F59E0B;"></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 9. MAIN MULTI-VIEW WORKSPACE
# -----------------------------------------------------------------------------
tab_pbi, tab_sql, tab_geo, tab_raw, tab_biz = st.tabs([
    "📊 Power BI Analytics Suite (5 Views)",
    "⚡ SQL Query Studio & Console",
    "🗺️ Geospatial & Route Flow",
    "🔍 Cleaned Data Explorer",
    "💡 Strategic Executive Playbook"
])


# =============================================================================
# TAB 1: POWER BI ANALYTICS SUITE (EXACT 5 SEGREGATED VIEWS)
# =============================================================================
with tab_pbi:
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
        <h3 style="margin: 0; color: #FFFFFF; font-size: 1.3rem; font-weight: 700;">
            📊 Power BI Dashboard Analytics Suite
        </h3>
        <span style="background: rgba(178,255,0,0.12); color: #B2FF00; border: 1px solid rgba(178,255,0,0.3); font-size: 0.75rem; font-weight: 700; padding: 4px 10px; border-radius: 6px;">
            5 Segregated Views
        </span>
    </div>
    """, unsafe_allow_html=True)

    v1, v2, v3, v4, v5 = st.tabs([
        "1. Overall View",
        "2. Vehicle Type View",
        "3. Revenue View",
        "4. Cancellation View",
        "5. Ratings View"
    ])

    # -------------------------------------------------------------------------
    # VIEW 1: OVERALL VIEW
    # -------------------------------------------------------------------------
    with v1:
        st.markdown("""
        <div class="chart-desc">
            Macro-level analysis tracking daily ride booking velocity and overall fulfillment health.
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([7, 5])
        
        with col1:
            st.markdown("""
            <div class="chart-card">
                <div class="chart-title">📈 Ride Volume Over Time (Daily Trajectory)</div>
                <div class="chart-desc">Daily demand volume tracking completed trips vs total requests.</div>
            </div>
            """, unsafe_allow_html=True)
            
            daily_total = filtered_df.groupby('Ride_Date').size().reset_index(name='Total_Rides')
            daily_success = filtered_df[filtered_df['Booking_Status'] == 'Success'].groupby('Ride_Date').size().reset_index(name='Completed_Rides')
            daily_merged = pd.merge(daily_total, daily_success, on='Ride_Date', how='left').fillna(0)
            
            fig_trend = go.Figure()
            fig_trend.add_trace(go.Scatter(
                x=daily_merged['Ride_Date'],
                y=daily_merged['Total_Rides'],
                mode='lines+markers',
                name='Total Requests',
                line=dict(color='#B2FF00', width=3),
                marker=dict(size=6, color='#B2FF00'),
                fill='tozeroy',
                fillcolor='rgba(178, 255, 0, 0.05)'
            ))
            fig_trend.add_trace(go.Scatter(
                x=daily_merged['Ride_Date'],
                y=daily_merged['Completed_Rides'],
                mode='lines+markers',
                name='Successful Trips',
                line=dict(color='#10B981', width=2, dash='dot'),
                marker=dict(size=4, color='#10B981')
            ))
            fig_trend = apply_chart_style(fig_trend, height=360)
            fig_trend.update_layout(hovermode='x unified')
            st.plotly_chart(fig_trend, use_container_width=True)

        with col2:
            st.markdown("""
            <div class="chart-card">
                <div class="chart-title">🎯 Booking Status Breakdown</div>
                <div class="chart-desc">Fulfillment split across success, driver/customer cancellation, and supply gaps.</div>
            </div>
            """, unsafe_allow_html=True)
            
            status_counts = filtered_df['Booking_Status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']
            
            status_colors = {
                'Success': '#10B981',
                'Canceled by Driver': '#F43F5E',
                'Canceled by Customer': '#F97316',
                'Driver Not Found': '#64748B'
            }
            
            fig_status = px.pie(
                status_counts,
                names='Status',
                values='Count',
                hole=0.6,
                color='Status',
                color_discrete_map=status_colors
            )
            fig_status.update_traces(
                textposition='inside',
                textinfo='percent+label',
                marker=dict(line=dict(color='#080B11', width=2))
            )
            fig_status = apply_chart_style(fig_status, height=360)
            st.plotly_chart(fig_status, use_container_width=True)

        # Hourly Distribution Profile
        st.markdown("""
        <div class="chart-card">
            <div class="chart-title">⏰ 24-Hour Demand Curve & Peak Hours</div>
            <div class="chart-desc">Identifies morning (08:00 - 11:00) and evening rush hours (17:00 - 21:00) for dynamic surge planning.</div>
        </div>
        """, unsafe_allow_html=True)
        
        hourly_split = filtered_df.groupby(['Ride_Hour', 'Booking_Status']).size().reset_index(name='Count')
        fig_hour = px.bar(
            hourly_split,
            x='Ride_Hour',
            y='Count',
            color='Booking_Status',
            color_discrete_map=status_colors,
            barmode='stack',
            labels={'Ride_Hour': 'Hour of Day (24-Hour Format)', 'Count': 'Trips'}
        )
        fig_hour = apply_chart_style(fig_hour, height=340)
        fig_hour.update_layout(xaxis=dict(tickmode='linear', tick0=0, dtick=1))
        st.plotly_chart(fig_hour, use_container_width=True)

    # -------------------------------------------------------------------------
    # VIEW 2: VEHICLE TYPE VIEW
    # -------------------------------------------------------------------------
    with v2:
        st.markdown("""
        <div class="chart-desc">
            Fleet composition, ride distance profiles, and vehicle turnaround times (TAT) across 7 categories.
        </div>
        """, unsafe_allow_html=True)
        
        vc1, vc2 = st.columns([7, 5])
        
        with vc1:
            st.markdown("""
            <div class="chart-card">
                <div class="chart-title">🚗 Top 5 Vehicle Types by Ride Distance</div>
                <div class="chart-desc">Average trip length (km) benchmarked across vehicle tiers.</div>
            </div>
            """, unsafe_allow_html=True)
            
            veh_dist = filtered_df.groupby('Vehicle_Type').agg(
                Avg_Distance=('Ride_Distance', 'mean'),
                Total_Distance=('Ride_Distance', 'sum'),
                Trip_Count=('Booking_ID', 'count')
            ).reset_index().sort_values(by='Avg_Distance', ascending=True)
            
            fig_veh_dist = px.bar(
                veh_dist,
                y='Vehicle_Type',
                x='Avg_Distance',
                orientation='h',
                text='Avg_Distance',
                color='Avg_Distance',
                color_continuous_scale=[[0, '#06B6D4'], [0.5, '#3B82F6'], [1, '#B2FF00']],
                labels={'Avg_Distance': 'Avg Distance (km)', 'Vehicle_Type': 'Vehicle Category'}
            )
            fig_veh_dist.update_traces(
                texttemplate='%{text:.2f} km',
                textposition='outside',
                marker=dict(line=dict(color='rgba(255,255,255,0.1)', width=1))
            )
            fig_veh_dist = apply_chart_style(fig_veh_dist, height=360)
            fig_veh_dist.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig_veh_dist, use_container_width=True)

        with vc2:
            st.markdown("""
            <div class="chart-card">
                <div class="chart-title">🚕 Fleet Volume Distribution</div>
                <div class="chart-desc">Market share across Auto, Bike, Sedan, SUV, and Mini fleets.</div>
            </div>
            """, unsafe_allow_html=True)
            
            veh_counts = filtered_df['Vehicle_Type'].value_counts().reset_index()
            veh_counts.columns = ['Vehicle_Type', 'Trips']
            
            fig_v_share = px.pie(
                veh_counts,
                names='Vehicle_Type',
                values='Trips',
                hole=0.55,
                color_discrete_sequence=['#B2FF00', '#06B6D4', '#10B981', '#8B5CF6', '#F59E0B', '#3B82F6', '#EC4899']
            )
            fig_v_share.update_traces(textposition='inside', textinfo='percent+label')
            fig_v_share = apply_chart_style(fig_v_share, height=360)
            st.plotly_chart(fig_v_share, use_container_width=True)

        # Operational TAT Performance
        st.markdown("""
        <div class="chart-card">
            <div class="chart-title">⏱️ Turnaround Times: Vehicle TAT (V_TAT) vs. Customer TAT (C_TAT)</div>
            <div class="chart-desc">Turnaround time in seconds to evaluate dispatch latency and rider boarding efficiency.</div>
        </div>
        """, unsafe_allow_html=True)
        
        tat_summary = success_records.groupby('Vehicle_Type')[['V_TAT', 'C_TAT']].mean().reset_index()
        fig_tat = px.bar(
            tat_summary,
            x='Vehicle_Type',
            y=['V_TAT', 'C_TAT'],
            barmode='group',
            color_discrete_map={'V_TAT': '#06B6D4', 'C_TAT': '#F43F5E'},
            labels={'value': 'Seconds', 'variable': 'TAT Metric', 'Vehicle_Type': 'Vehicle Category'}
        )
        fig_tat = apply_chart_style(fig_tat, height=340)
        st.plotly_chart(fig_tat, use_container_width=True)

    # -------------------------------------------------------------------------
    # VIEW 3: REVENUE VIEW
    # -------------------------------------------------------------------------
    with v3:
        st.markdown("""
        <div class="chart-desc">
            Gross merchandise value (GMV), payment channel adoption, and top VIP spenders.
        </div>
        """, unsafe_allow_html=True)
        
        rc1, rc2 = st.columns([6, 6])
        
        with rc1:
            st.markdown("""
            <div class="chart-card">
                <div class="chart-title">💳 Revenue by Payment Method</div>
                <div class="chart-desc">Cash vs UPI vs Credit/Debit Card contributions.</div>
            </div>
            """, unsafe_allow_html=True)
            
            pm_rev = success_records.groupby('Payment_Method').agg(
                Revenue=('Booking_Value', 'sum'),
                Count=('Booking_ID', 'count')
            ).reset_index().sort_values(by='Revenue', ascending=False)
            
            fig_pm = px.pie(
                pm_rev,
                names='Payment_Method',
                values='Revenue',
                hole=0.6,
                color_discrete_sequence=['#10B981', '#B2FF00', '#06B6D4', '#8B5CF6']
            )
            fig_pm.update_traces(
                textposition='inside',
                textinfo='percent+label',
                marker=dict(line=dict(color='#080B11', width=2))
            )
            fig_pm = apply_chart_style(fig_pm, height=360)
            st.plotly_chart(fig_pm, use_container_width=True)

        with rc2:
            st.markdown("""
            <div class="chart-card">
                <div class="chart-title">👑 Top 5 Customers by Total Booking Value</div>
                <div class="chart-desc">Highest lifetime value (LTV) patrons in July 2024.</div>
            </div>
            """, unsafe_allow_html=True)
            
            top_spenders = success_records.groupby('Customer_ID').agg(
                Total_Spent=('Booking_Value', 'sum'),
                Trips=('Booking_ID', 'count')
            ).reset_index().sort_values(by='Total_Spent', ascending=True).tail(5)
            
            fig_top_c = px.bar(
                top_spenders,
                y='Customer_ID',
                x='Total_Spent',
                orientation='h',
                text='Total_Spent',
                color='Total_Spent',
                color_continuous_scale=[[0, '#06B6D4'], [1, '#B2FF00']]
            )
            fig_top_c.update_traces(
                texttemplate='₹%{text:,}',
                textposition='outside',
                marker=dict(line=dict(color='rgba(255,255,255,0.1)', width=1))
            )
            fig_top_c = apply_chart_style(fig_top_c, height=360)
            fig_top_c.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig_top_c, use_container_width=True)

        # Ride Distance Distribution Per Day
        st.markdown("""
        <div class="chart-card">
            <div class="chart-title">📍 Ride Distance Distribution Per Day</div>
            <div class="chart-desc">Total fleet mileage (km) alongside daily average trip length.</div>
        </div>
        """, unsafe_allow_html=True)
        
        daily_dist = success_records.groupby('Ride_Date').agg(
            Total_Km=('Ride_Distance', 'sum'),
            Avg_Km=('Ride_Distance', 'mean')
        ).reset_index()
        
        fig_dual = go.Figure()
        fig_dual.add_trace(go.Bar(
            x=daily_dist['Ride_Date'],
            y=daily_dist['Total_Km'],
            name='Total Fleet Km',
            marker=dict(color='#06B6D4', opacity=0.85)
        ))
        fig_dual.add_trace(go.Scatter(
            x=daily_dist['Ride_Date'],
            y=daily_dist['Avg_Km'],
            name='Avg Trip Km',
            yaxis='y2',
            line=dict(color='#B2FF00', width=3)
        ))
        fig_dual = apply_chart_style(fig_dual, height=340)
        fig_dual.update_layout(
            yaxis=dict(title="Total Fleet Distance (km)"),
            yaxis2=dict(title="Average Distance (km)", overlaying='y', side='right', showgrid=False)
        )
        st.plotly_chart(fig_dual, use_container_width=True)

    # -------------------------------------------------------------------------
    # VIEW 4: CANCELLATION VIEW
    # -------------------------------------------------------------------------
    with v4:
        st.markdown("""
        <div class="chart-desc">
            Deep dive into customer and driver attrition, abort reasons, and mid-trip breakdowns.
        </div>
        """, unsafe_allow_html=True)
        
        canc_c1, canc_c2 = st.columns(2)
        
        with canc_c1:
            st.markdown("""
            <div class="chart-card">
                <div class="chart-title">👤 Cancelled Rides Reasons (Customer)</div>
                <div class="chart-desc">Root causes behind 10,499 customer cancellations.</div>
            </div>
            """, unsafe_allow_html=True)
            
            c_reasons = filtered_df['Canceled_Rides_by_Customer'].dropna().value_counts().reset_index()
            c_reasons.columns = ['Reason', 'Cancellations']
            
            fig_cr = px.bar(
                c_reasons.sort_values(by='Cancellations', ascending=True),
                y='Reason',
                x='Cancellations',
                orientation='h',
                text='Cancellations',
                color='Cancellations',
                color_continuous_scale=[[0, '#F97316'], [1, '#EF4444']]
            )
            fig_cr.update_traces(texttemplate='%{text:,}', textposition='outside')
            fig_cr = apply_chart_style(fig_cr, height=340)
            fig_cr.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig_cr, use_container_width=True)

        with canc_c2:
            st.markdown("""
            <div class="chart-card">
                <div class="chart-title">🚗 Cancelled Rides Reasons (Drivers)</div>
                <div class="chart-desc">Root causes behind 18,434 driver cancellations.</div>
            </div>
            """, unsafe_allow_html=True)
            
            d_reasons = filtered_df['Canceled_Rides_by_Driver'].dropna().value_counts().reset_index()
            d_reasons.columns = ['Reason', 'Cancellations']
            
            fig_dr = px.bar(
                d_reasons.sort_values(by='Cancellations', ascending=True),
                y='Reason',
                x='Cancellations',
                orientation='h',
                text='Cancellations',
                color='Cancellations',
                color_continuous_scale=[[0, '#F59E0B'], [1, '#DC2626']]
            )
            fig_dr.update_traces(texttemplate='%{text:,}', textposition='outside')
            fig_dr = apply_chart_style(fig_dr, height=340)
            fig_dr.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig_dr, use_container_width=True)

        # Incomplete Rides
        st.markdown("""
        <div class="chart-card">
            <div class="chart-title">⚠️ Incomplete Rides Breakdown (3,926 Trips Terminated Mid-Journey)</div>
            <div class="chart-desc">Breakdowns vs Rider early exit requests.</div>
        </div>
        """, unsafe_allow_html=True)
        
        inc_reasons = filtered_df[filtered_df['Incomplete_Rides'] == 'Yes']['Incomplete_Rides_Reason'].value_counts().reset_index()
        inc_reasons.columns = ['Reason', 'Count']
        
        in1, in2 = st.columns([5, 7])
        with in1:
            fig_inc_pie = px.pie(
                inc_reasons,
                names='Reason',
                values='Count',
                hole=0.55,
                color_discrete_sequence=['#F43F5E', '#F59E0B', '#8B5CF6']
            )
            fig_inc_pie = apply_chart_style(fig_inc_pie, height=300)
            st.plotly_chart(fig_inc_pie, use_container_width=True)
            
        with in2:
            st.markdown("""
            <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(244, 63, 94, 0.3); border-left: 4px solid #F43F5E; border-radius: 10px; padding: 18px; margin-top: 20px;">
                <h5 style="color: #F43F5E; margin: 0 0 10px 0;">Operational Impact of Incomplete Trips</h5>
                <p style="color: #CBD5E1; font-size: 0.88rem; line-height: 1.7; margin: 0;">
                    • <b>Customer Demand (40.78% / 1,601 trips):</b> Passengers exiting early due to traffic or itinerary shifts.<br>
                    • <b>Vehicle Breakdown (40.52% / 1,591 trips):</b> Urgent fleet health signal requiring scheduled maintenance hubs.<br>
                    • <b>Other Issues (18.70% / 734 trips):</b> Extreme weather or localized routing disputes.
                </p>
            </div>
            """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # VIEW 5: RATINGS VIEW
    # -------------------------------------------------------------------------
    with v5:
        st.markdown("""
        <div class="chart-desc">
            Customer trust, driver performance ratings, and inter-category quality consistency.
        </div>
        """, unsafe_allow_html=True)
        
        rat1, rat2 = st.columns(2)
        
        with rat1:
            st.markdown("""
            <div class="chart-card">
                <div class="chart-title">⭐ Driver Ratings Distribution</div>
                <div class="chart-desc">Scores given by passengers to drivers (Citywide Avg: 4.00 / 5).</div>
            </div>
            """, unsafe_allow_html=True)
            
            fig_d_hist = px.histogram(
                success_records,
                x='Driver_Ratings',
                nbins=20,
                color_discrete_sequence=['#06B6D4']
            )
            fig_d_hist = apply_chart_style(fig_d_hist, height=320)
            fig_d_hist.update_layout(xaxis_title="Driver Rating Score", yaxis_title="Number of Trips")
            st.plotly_chart(fig_d_hist, use_container_width=True)

        with rat2:
            st.markdown("""
            <div class="chart-card">
                <div class="chart-title">⭐ Customer Ratings Distribution</div>
                <div class="chart-desc">Scores given by drivers to customers (Citywide Avg: 4.00 / 5).</div>
            </div>
            """, unsafe_allow_html=True)
            
            fig_c_hist = px.histogram(
                success_records,
                x='Customer_Rating',
                nbins=20,
                color_discrete_sequence=['#B2FF00']
            )
            fig_c_hist = apply_chart_style(fig_c_hist, height=320)
            fig_c_hist.update_layout(xaxis_title="Customer Rating Score", yaxis_title="Number of Trips")
            st.plotly_chart(fig_c_hist, use_container_width=True)

        # Customer vs Driver Ratings Comparison
        st.markdown("""
        <div class="chart-card">
            <div class="chart-title">⚖️ Customer vs. Driver Ratings by Vehicle Category</div>
            <div class="chart-desc">Comparing passenger and driver experience across each fleet class.</div>
        </div>
        """, unsafe_allow_html=True)
        
        rating_comp = success_records.groupby('Vehicle_Type').agg(
            Customer_Rating=('Customer_Rating', 'mean'),
            Driver_Rating=('Driver_Ratings', 'mean')
        ).reset_index()
        
        fig_r_comp = px.bar(
            rating_comp,
            x='Vehicle_Type',
            y=['Customer_Rating', 'Driver_Rating'],
            barmode='group',
            color_discrete_map={'Customer_Rating': '#B2FF00', 'Driver_Rating': '#06B6D4'}
        )
        fig_r_comp = apply_chart_style(fig_r_comp, height=340)
        fig_r_comp.update_layout(yaxis=dict(range=[3.5, 4.3], title="Rating (Out of 5)"))
        st.plotly_chart(fig_r_comp, use_container_width=True)


# =============================================================================
# TAB 2: SQL QUERY STUDIO & WORKBENCH
# =============================================================================
with tab_sql:
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
        <h3 style="margin: 0; color: #FFFFFF; font-size: 1.3rem; font-weight: 700;">
            ⚡ SQL Query Studio & Execution Engine
        </h3>
        <span style="background: rgba(6,182,212,0.12); color: #06B6D4; border: 1px solid rgba(6,182,212,0.3); font-size: 0.75rem; font-weight: 700; padding: 4px 10px; border-radius: 6px;">
            SQLite B-Tree Accelerated
        </span>
    </div>
    """, unsafe_allow_html=True)

    sql_tab_pre, sql_tab_custom = st.tabs(["📋 Predefined Questions (1 to 10)", "✍️ Live SQL Terminal"])
    
    with sql_tab_pre:
        query_keys = list(PREDEFINED_SQL_QUERIES.keys())
        chosen_q = st.selectbox("🎯 Select Project SQL Question to Inspect & Run:", options=query_keys)
        
        q_data = PREDEFINED_SQL_QUERIES[chosen_q]
        
        st.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid var(--card-border); border-radius: 10px; padding: 16px; margin: 12px 0;">
            <div style="color: #B2FF00; font-size: 0.75rem; font-weight: 700; text-transform: uppercase;">Question #{q_data['id']}</div>
            <div style="color: #FFFFFF; font-size: 1.05rem; font-weight: 700; margin: 4px 0 8px 0;">{q_data['question']}</div>
            <div style="color: #94A3B8; font-size: 0.85rem;">{q_data['description']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("##### 📝 SQL Statement:")
        st.code(q_data['sql'], language="sql")
        
        c_left, c_right = st.columns([8, 4])
        with c_right:
            st.markdown(f"""
            <div style="background: rgba(6, 182, 212, 0.1); border: 1px solid rgba(6, 182, 212, 0.25); border-radius: 10px; padding: 14px; font-size: 0.82rem; line-height: 1.6; color: #E2E8F0;">
                <b style="color: #06B6D4;">Expected Result:</b><br>{q_data['expected_result']}
            </div>
            """, unsafe_allow_html=True)
            
        with c_left:
            if st.button(f"⚡ Execute Query {q_data['id']} Now", key=f"run_q_{q_data['id']}"):
                with st.spinner("Executing query on SQLite..."):
                    run_sql = q_data.get("count_sql") or q_data.get("breakdown_sql") or q_data["sql"]
                    if "LIMIT" not in run_sql and ("SELECT *" in run_sql or "SELECT Booking_ID" in run_sql):
                        run_sql = q_data["sql"] + " LIMIT 100"
                        st.caption("ℹ️ Displaying first 100 records for optimal UI rendering.")
                    
                    df_out, row_cnt, exec_ms, sql_err = execute_query(run_sql)
                    if sql_err:
                        st.error(f"SQL Error: {sql_err}")
                    else:
                        st.markdown(f"""
                        <div style="display: flex; gap: 12px; margin-bottom: 10px;">
                            <span style="background: rgba(16, 185, 129, 0.15); color: #10B981; border: 1px solid rgba(16, 185, 129, 0.3); padding: 4px 10px; border-radius: 6px; font-size: 0.78rem; font-weight: 700;">
                                ✓ Returned {row_cnt:,} rows
                            </span>
                            <span style="background: rgba(178, 255, 0, 0.15); color: #B2FF00; border: 1px solid rgba(178, 255, 0, 0.3); padding: 4px 10px; border-radius: 6px; font-size: 0.78rem; font-weight: 700;">
                                ⚡ Executed in {exec_ms} ms
                            </span>
                        </div>
                        """, unsafe_allow_html=True)
                        st.dataframe(df_out, use_container_width=True)
                        
                        csv_bytes = df_out.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label=f"📥 Download Query {q_data['id']} Results (CSV)",
                            data=csv_bytes,
                            file_name=f"ola_query_{q_data['id']}_result.csv",
                            mime="text/csv"
                        )

    with sql_tab_custom:
        st.markdown("##### ✍️ Custom SQL Query Console (Query table `rides`):")
        
        sample_q = """-- Peak demand origin nodes
SELECT Pickup_Location, 
       COUNT(*) AS Total_Requests, 
       ROUND(SUM(CASE WHEN Booking_Status = 'Success' THEN Booking_Value ELSE 0 END)/1e3, 2) AS Revenue_K_INR
FROM rides 
GROUP BY Pickup_Location 
ORDER BY Total_Requests DESC 
LIMIT 10;"""
        
        custom_input = st.text_area("SQL Terminal Input:", value=sample_q, height=140)
        
        if st.button("🚀 Run Terminal SQL", key="exec_custom_btn"):
            with st.spinner("Processing SQL query..."):
                c_df, c_len, c_ms, c_err = execute_query(custom_input)
                if c_err:
                    st.error(f"SQL Execution Error: {c_err}")
                else:
                    st.success(f"Success! {c_len:,} rows returned in {c_ms} ms.")
                    st.dataframe(c_df, use_container_width=True)


# =============================================================================
# TAB 3: GEOSPATIAL & ROUTE FLOW
# =============================================================================
with tab_geo:
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
        <h3 style="margin: 0; color: #FFFFFF; font-size: 1.3rem; font-weight: 700;">
            🗺️ Geospatial Demand Hotspots & Route Corridors
        </h3>
        <span style="background: rgba(139,92,246,0.12); color: #8B5CF6; border: 1px solid rgba(139,92,246,0.3); font-size: 0.75rem; font-weight: 700; padding: 4px 10px; border-radius: 6px;">
            Bengaluru Top Nodes
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    g1, g2 = st.columns(2)
    
    with g1:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-title">📍 Top 10 Origin Zones (Highest Ride Requests)</div>
            <div class="chart-desc">Key pickup nodes requiring proactive fleet staging.</div>
        </div>
        """, unsafe_allow_html=True)
        
        top_origins = filtered_df['Pickup_Location'].value_counts().head(10).reset_index()
        top_origins.columns = ['Pickup_Location', 'Requests']
        
        fig_origin = px.bar(
            top_origins.sort_values(by='Requests', ascending=True),
            y='Pickup_Location',
            x='Requests',
            orientation='h',
            text='Requests',
            color='Requests',
            color_continuous_scale=[[0, '#06B6D4'], [1, '#B2FF00']]
        )
        fig_origin.update_traces(textposition='outside')
        fig_origin = apply_chart_style(fig_origin, height=360)
        fig_origin.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_origin, use_container_width=True)

    with g2:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-title">🏁 Top 10 Destination Hubs (Highest Traffic Flow)</div>
            <div class="chart-desc">Terminal zones generating concentrated drop-offs.</div>
        </div>
        """, unsafe_allow_html=True)
        
        top_dest = filtered_df['Drop_Location'].value_counts().head(10).reset_index()
        top_dest.columns = ['Drop_Location', 'Drop_Volume']
        
        fig_dest = px.bar(
            top_dest.sort_values(by='Drop_Volume', ascending=True),
            y='Drop_Location',
            x='Drop_Volume',
            orientation='h',
            text='Drop_Volume',
            color='Drop_Volume',
            color_continuous_scale=[[0, '#8B5CF6'], [1, '#EC4899']]
        )
        fig_dest.update_traces(textposition='outside')
        fig_dest = apply_chart_style(fig_dest, height=360)
        fig_dest.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_dest, use_container_width=True)

    # Top O-D Route Corridors
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">🔁 High-Traffic Route Corridors (Origin ➡️ Destination)</div>
        <div class="chart-desc">Most heavily travelled commuter lines in Bengaluru.</div>
    </div>
    """, unsafe_allow_html=True)
    
    route_traffic = filtered_df.groupby(['Pickup_Location', 'Drop_Location']).agg(
        Total_Trips=('Booking_ID', 'count'),
        Completed=('Booking_Status', lambda x: (x == 'Success').sum()),
        Total_Revenue=('Booking_Value', lambda x: x[filtered_df.loc[x.index, 'Booking_Status'] == 'Success'].sum())
    ).reset_index().sort_values(by='Total_Trips', ascending=False).head(10)
    
    st.dataframe(route_traffic, use_container_width=True)


# =============================================================================
# TAB 4: RAW DATA EXPLORER
# =============================================================================
with tab_raw:
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
        <h3 style="margin: 0; color: #FFFFFF; font-size: 1.3rem; font-weight: 700;">
            🔍 Raw Data Explorer & Export Engine
        </h3>
        <span style="background: rgba(16,185,129,0.12); color: #10B981; border: 1px solid rgba(16,185,129,0.3); font-size: 0.75rem; font-weight: 700; padding: 4px 10px; border-radius: 6px;">
            {:,} Records Filtered
        </span>
    </div>
    """.format(len(filtered_df)), unsafe_allow_html=True)
    
    col_filter_choice = st.multiselect(
        "Select Fields to Display:",
        options=filtered_df.columns.tolist(),
        default=['Booking_ID', 'Ride_Date', 'Time_Str', 'Booking_Status', 'Customer_ID', 
                 'Vehicle_Type', 'Pickup_Location', 'Drop_Location', 'Booking_Value', 'Ride_Distance']
    )
    
    st.dataframe(filtered_df[col_filter_choice].head(1000), use_container_width=True)
    st.caption("Displaying preview of first 1,000 records. Download full subset below.")
    
    raw_csv = filtered_df[col_filter_choice].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Filtered Subset (CSV)",
        data=raw_csv,
        file_name="ola_filtered_export.csv",
        mime="text/csv"
    )


# =============================================================================
# TAB 5: STRATEGIC BUSINESS PLAYBOOK
# =============================================================================
with tab_biz:
    st.markdown("""
    <div style="margin-bottom: 18px;">
        <h3 style="margin: 0 0 4px 0; color: #FFFFFF; font-size: 1.3rem; font-weight: 700;">
            💡 Strategic Executive Playbook & Operational Roadmap
        </h3>
        <p style="color: #94A3B8; font-size: 0.9rem; margin: 0;">
            High-impact operational recommendations derived from empirical analysis of 103,024 rides.
        </p>
    </div>
    """, unsafe_allow_html=True)

    b1, b2 = st.columns(2)
    
    with b1:
        st.markdown("""
        <div class="strategy-card" style="border-left: 4px solid var(--ola-lime);">
            <div class="strategy-pill" style="background: rgba(178,255,0,0.15); color: var(--ola-lime);">
                Supply Rebalancing & Surge Pricing
            </div>
            <h4 style="color: #FFFFFF; margin: 0 0 10px 0;">1. Solve the 9.8% 'Driver Not Found' Gap</h4>
            <p style="color: #CBD5E1; font-size: 0.88rem; line-height: 1.7;">
                <b>Empirical Finding:</b> 10,124 bookings went completely unfulfilled due to <i>'Driver Not Found'</i>, representing over ₹5.5M in lost GMV.<br>
                <b>Actionable Protocol:</b>
                <ul style="color: #94A3B8; padding-left: 20px;">
                    <li>Implement algorithmic rebalancing dispatch: incentivize idle cabs from low-demand sectors to relocate to Banashankari & Yeshwanthpur prior to evening rush (17:00).</li>
                    <li>Activate dynamic micro-surge multipliers (1.15x - 1.25x) during the 18:00 - 21:00 peak to expand active driver supply.</li>
                </ul>
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="strategy-card" style="border-left: 4px solid #F43F5E;">
            <div class="strategy-pill" style="background: rgba(244,63,94,0.15); color: #F43F5E;">
                Attrition Mitigation
            </div>
            <h4 style="color: #FFFFFF; margin: 0 0 10px 0;">2. Driver Cancellation Reduction Playbook</h4>
            <p style="color: #CBD5E1; font-size: 0.88rem; line-height: 1.7;">
                <b>Empirical Finding:</b> Drivers initiated 18,434 cancellations (17.89% of all rides), with 35.5% citing <i>'Personal & Car related issue'</i>.<br>
                <b>Actionable Protocol:</b>
                <ul style="color: #94A3B8; padding-left: 20px;">
                    <li>Establish rapid pit-stop vehicle maintenance facilities near top drop-off zones to resolve mechanical issues.</li>
                    <li>Introduce trip streak completion incentives: drivers who complete 6 consecutive rides without voluntary cancellation earn 15% bonus fare.</li>
                </ul>
            </p>
        </div>
        """, unsafe_allow_html=True)

    with b2:
        st.markdown("""
        <div class="strategy-card" style="border-left: 4px solid #06B6D4;">
            <div class="strategy-pill" style="background: rgba(6,182,212,0.15); color: #06B6D4;">
                Passenger Retention
            </div>
            <h4 style="color: #FFFFFF; margin: 0 0 10px 0;">3. Live Movement Tracking & Anti-Wait Friction</h4>
            <p style="color: #CBD5E1; font-size: 0.88rem; line-height: 1.7;">
                <b>Empirical Finding:</b> 30.2% of customer cancellations (3,175 rides) occurred because the driver was stationary or moving away from pickup.<br>
                <b>Actionable Protocol:</b>
                <ul style="color: #94A3B8; padding-left: 20px;">
                    <li>Deploy proactive stationary alerts: if a driver shows zero GPS displacement for 180 seconds after accepting, prompt driver and alert rider with re-dispatch option.</li>
                    <li>Provide transparent live traffic-adjusted ETA countdowns to curb anxiety cancellations.</li>
                </ul>
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="strategy-card" style="border-left: 4px solid #F59E0B;">
            <div class="strategy-pill" style="background: rgba(245,158,11,0.15); color: #F59E0B;">
                Fintech Acceleration
            </div>
            <h4 style="color: #FFFFFF; margin: 0 0 10px 0;">4. Digital Settlement & UPI AutoPay Push</h4>
            <p style="color: #CBD5E1; font-size: 0.88rem; line-height: 1.7;">
                <b>Empirical Finding:</b> Cash still commands 54.9% (₹19.26M) of settled revenue, creating change disputes and end-of-trip delays.<br>
                <b>Actionable Protocol:</b>
                <ul style="color: #94A3B8; padding-left: 20px;">
                    <li>Incentivize UPI AutoPay setup with ₹25 instant cashback on the first 3 digital rides.</li>
                    <li>Target shifting digital transaction share from 45.1% to > 70% within two quarters.</li>
                </ul>
            </p>
        </div>
        """, unsafe_allow_html=True)
