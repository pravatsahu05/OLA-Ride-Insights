"""
=============================================================================
OLA RIDE INSIGHTS - ADVANCED MOBILITY CONTROL CENTER
Theme: Dark Obsidian & Electric Volt Neon Lime (#D4FF00) matching Next-Gen Mobility UI
Features: Clean, interactive dashboard without unclickable pseudo-buttons,
flattened navigation for instant access, and dedicated insights & business actions under every visual.
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
    page_title="OLA Mobility OS | Executive Control Deck",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------------------
# 2. EXACT THEME STYLING: MATTE OBSIDIAN & ELECTRIC VOLT LIME (#D4FF00)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    :root {
        --volt-lime: #D4FF00;
        --volt-lime-glow: rgba(212, 255, 0, 0.32);
        --bg-black: #0B0C10;
        --card-bg: #15161C;
        --card-surface: #1B1D24;
        --card-border: rgba(255, 255, 255, 0.06);
        --card-hover-border: rgba(212, 255, 0, 0.35);
        --text-white: #FFFFFF;
        --text-muted: #8E929E;
        --text-dim: #5F6370;
        --pill-inactive: #23252E;
        --accent-emerald: #10B981;
        --accent-rose: #FF3B56;
        --accent-amber: #FFB800;
        --accent-cyan: #00F0FF;
    }

    /* Base Page Styling */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text-white);
    }
    
    .stApp {
        background-color: var(--bg-black);
    }

    /* Completely Hide Sidebar */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Scrollbars */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: var(--bg-black);
    }
    ::-webkit-scrollbar-thumb {
        background: #23252E;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--volt-lime);
    }

    /* UNIFIED CONTAINER CARD: Wraps Header, Chart & Insights seamlessly into ONE card */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 20px !important;
        padding: 20px 22px 18px 22px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35) !important;
    }

    /* Header Nav Banner */
    .top-navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 18px 26px;
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 20px;
        margin-bottom: 22px;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4);
    }
    .brand-group {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .brand-logo-icon {
        background: var(--volt-lime);
        color: #000000;
        width: 44px;
        height: 44px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.4rem;
        font-weight: 900;
        box-shadow: 0 0 22px var(--volt-lime-glow);
    }
    .brand-name {
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #FFFFFF;
        margin: 0;
        line-height: 1.1;
    }
    .brand-name span {
        color: var(--volt-lime);
    }
    .brand-tagline {
        color: var(--text-muted);
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 2px;
    }
    .live-dot {
        width: 8px;
        height: 8px;
        background-color: var(--volt-lime);
        border-radius: 50%;
        box-shadow: 0 0 12px var(--volt-lime);
        animation: pulseLive 2s infinite;
    }
    @keyframes pulseLive {
        0% { transform: scale(0.9); opacity: 0.7; }
        50% { transform: scale(1.3); opacity: 1; }
        100% { transform: scale(0.9); opacity: 0.7; }
    }

    /* Card Inside Elements */
    .card-title-text {
        font-size: 1.05rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 2px;
    }
    .card-subtitle-text {
        font-size: 0.82rem;
        color: var(--text-muted);
        margin-bottom: 12px;
    }

    /* KPI Cards Styling */
    .theme-kpi-card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 20px;
        padding: 18px 20px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
    }
    .kpi-card-header {
        margin-bottom: 8px;
    }
    .kpi-card-label {
        font-size: 0.74rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        color: var(--text-muted);
    }
    .kpi-card-num {
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #FFFFFF;
        line-height: 1;
        margin-bottom: 6px;
    }
    .kpi-card-sub {
        font-size: 0.78rem;
        color: var(--text-dim);
    }
    .capsule-track {
        width: 100%;
        height: 5px;
        background: #23252E;
        border-radius: 10px;
        margin-top: 10px;
        overflow: hidden;
    }
    .capsule-fill {
        height: 100%;
        border-radius: 10px;
        background: var(--volt-lime);
        box-shadow: 0 0 10px var(--volt-lime-glow);
    }

    /* Dedicated Insight & Recommendation Box */
    .insight-box {
        background: #0E0F14;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-left: 3px solid var(--volt-lime);
        border-radius: 12px;
        padding: 12px 16px;
        margin-top: 12px;
        display: flex;
        flex-direction: column;
        gap: 6px;
    }
    .insight-row {
        display: flex;
        align-items: baseline;
        gap: 10px;
        font-size: 0.85rem;
        line-height: 1.45;
    }
    .badge-insight {
        background: rgba(212, 255, 0, 0.15);
        color: var(--volt-lime);
        font-size: 0.7rem;
        font-weight: 800;
        padding: 2px 8px;
        border-radius: 6px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        white-space: nowrap;
    }
    .badge-recom {
        background: rgba(16, 185, 129, 0.15);
        color: var(--accent-emerald);
        font-size: 0.7rem;
        font-weight: 800;
        padding: 2px 8px;
        border-radius: 6px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        white-space: nowrap;
    }
    .insight-text {
        color: #E2E8F0;
    }
    .recom-text {
        color: #CBD5E1;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #111216;
        padding: 6px;
        border-radius: 16px;
        border: 1px solid var(--card-border);
        margin-bottom: 18px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px !important;
        padding: 10px 20px !important;
        font-size: 0.88rem !important;
        font-weight: 700 !important;
        color: var(--text-muted) !important;
        border: none !important;
        background: transparent !important;
        transition: all 0.2s ease !important;
    }
    .stTabs [aria-selected="true"] {
        background: var(--volt-lime) !important;
        color: #000000 !important;
        box-shadow: 0 4px 16px var(--volt-lime-glow) !important;
    }

    /* Form Controls & Buttons Styling */
    .stButton>button {
        background-color: var(--volt-lime) !important;
        color: #000000 !important;
        font-weight: 700 !important;
        border-radius: 30px !important;
        border: none !important;
        padding: 8px 24px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 16px rgba(212, 255, 0, 0.2) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(212, 255, 0, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 3. FAST CACHED MASTER DATA PIPELINE
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
# 4. PLOTLY UNIFIED DARK OBSIDIAN + NEON LIME THEME
# -----------------------------------------------------------------------------
def apply_theme_plot(fig, height=340):
    fig.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=15, r=15, t=25, b=15),
        font=dict(family="Plus Jakarta Sans", size=12, color="#8E929E"),
        hoverlabel=dict(
            bgcolor="#1A1C23",
            bordercolor="#D4FF00",
            font=dict(family="Plus Jakarta Sans", size=12, color="#FFFFFF")
        ),
        xaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.04)",
            linecolor="rgba(255, 255, 255, 0.06)",
            tickfont=dict(color="#8E929E")
        ),
        yaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.04)",
            linecolor="rgba(255, 255, 255, 0.06)",
            tickfont=dict(color="#8E929E")
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
# 5. TOP NAVBAR & BRANDING BANNER
# -----------------------------------------------------------------------------
st.markdown("""
<div class="top-navbar">
    <div class="brand-group">
        <div class="brand-logo-icon">⚡</div>
        <div>
            <div class="brand-name">OLA <span>MOBILITY</span> OS</div>
            <div class="brand-tagline">Bengaluru Urban Telemetry & Executive Business Intelligence</div>
        </div>
    </div>
    <div style="display: flex; align-items: center; gap: 8px; font-size: 0.8rem; color: #8E929E;">
        <span class="live-dot"></span>
        <span>103,024 Records Analyzed • July 2024</span>
    </div>
</div>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 6. TOP FILTER CONSOLE DECK (UNIFIED CONTAINER CARD)
# -----------------------------------------------------------------------------
with st.container(border=True):
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; padding-bottom: 6px; border-bottom: 1px solid rgba(255,255,255,0.04);">
        <span style="font-size: 0.8rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.6px; color: #8E929E;">
            🎛️ GLOBAL TELEMETRY FILTER CONSOLE
        </span>
        <span style="color: #D4FF00; font-size: 0.72rem; font-weight: 800; letter-spacing: 0.5px;">
            METRO CLUSTER: BENGALURU URBAN (50 HUBS)
        </span>
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


# -----------------------------------------------------------------------------
# 7. FILTER APPLICATION
# -----------------------------------------------------------------------------
filtered_df = master_df.copy()

if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
    s_date, e_date = selected_dates
    filtered_df = filtered_df[(filtered_df['Ride_Date'] >= s_date) & (filtered_df['Ride_Date'] <= e_date)]
elif isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 1:
    filtered_df = filtered_df[filtered_df['Ride_Date'] >= selected_dates[0]]

if selected_vehicles:
    filtered_df = filtered_df[filtered_df['Vehicle_Type'].isin(selected_vehicles)]

if selected_statuses:
    filtered_df = filtered_df[filtered_df['Booking_Status'].isin(selected_statuses)]

if selected_payments and len(selected_payments) < len(payment_options):
    filtered_df = filtered_df[filtered_df['Payment_Method'].isin(selected_payments) | filtered_df['Payment_Method'].isna()]


# -----------------------------------------------------------------------------
# 8. TOP-TIER EXECUTIVE KPI CARDS (RESPONSIVE COLUMNS)
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

kc1, kc2, kc3, kc4, kc5, kc6 = st.columns(6)

with kc1:
    st.markdown(f"""
    <div class="theme-kpi-card">
        <div class="kpi-card-header">
            <span class="kpi-card-label">Total Demand</span>
        </div>
        <div class="kpi-card-num">{total_count:,}</div>
        <div class="kpi-card-sub">50 Bengaluru Hubs</div>
        <div class="capsule-track">
            <div class="capsule-fill" style="width: 100%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with kc2:
    st.markdown(f"""
    <div class="theme-kpi-card">
        <div class="kpi-card-header">
            <span class="kpi-card-label">Fulfillment</span>
        </div>
        <div class="kpi-card-num" style="color: #D4FF00;">{success_pct:.1f}%</div>
        <div class="kpi-card-sub"><span style="color: #D4FF00; font-weight: 700;">{successful_count:,}</span> Completed</div>
        <div class="capsule-track">
            <div class="capsule-fill" style="width: {min(success_pct, 100)}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with kc3:
    st.markdown(f"""
    <div class="theme-kpi-card">
        <div class="kpi-card-header">
            <span class="kpi-card-label">Gross GMV</span>
        </div>
        <div class="kpi-card-num">₹{total_gross_rev/1e6:.2f}M</div>
        <div class="kpi-card-sub">Avg Fare: <b>₹{avg_ride_fare:.1f}</b></div>
        <div class="capsule-track">
            <div class="capsule-fill" style="width: 82%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with kc4:
    st.markdown(f"""
    <div class="theme-kpi-card">
        <div class="kpi-card-header">
            <span class="kpi-card-label">Mean Distance</span>
        </div>
        <div class="kpi-card-num">{avg_ride_dist:.1f} <span style="font-size: 1rem; color: #8E929E;">km</span></div>
        <div class="kpi-card-sub">Citywide Commute</div>
        <div class="capsule-track">
            <div class="capsule-fill" style="width: 70%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with kc5:
    st.markdown(f"""
    <div class="theme-kpi-card">
        <div class="kpi-card-header">
            <span class="kpi-card-label">Cancellations</span>
        </div>
        <div class="kpi-card-num" style="color: #FF3B56;">{cancellation_pct:.1f}%</div>
        <div class="kpi-card-sub"><span style="color: #FF3B56; font-weight: 700;">{total_cancels:,}</span> Aborted</div>
        <div class="capsule-track">
            <div class="capsule-fill" style="width: {min(cancellation_pct, 100)}%; background: #FF3B56; box-shadow: 0 0 10px rgba(255, 59, 86, 0.4);"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with kc6:
    st.markdown(f"""
    <div class="theme-kpi-card">
        <div class="kpi-card-header">
            <span class="kpi-card-label">Quality Score</span>
        </div>
        <div class="kpi-card-num">{avg_c_rating:.2f} <span style="font-size: 1rem; color: #8E929E;">/ 5</span></div>
        <div class="kpi-card-sub">Driver: <b>{avg_d_rating:.2f}</b></div>
        <div class="capsule-track">
            <div class="capsule-fill" style="width: {(avg_c_rating/5)*100:.1f}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 9. DIRECT, STREAMLINED NAVIGATION TABS (ALL TABS ARE FUNCTIONAL)
# -----------------------------------------------------------------------------
tab_overall, tab_veh, tab_rev, tab_canc, tab_rat, tab_sql, tab_geo, tab_raw = st.tabs([
    "📊 Overall View",
    "🚗 Vehicle Type View",
    "💳 Revenue View",
    "⚠️ Cancellation View",
    "⭐ Ratings View",
    "⚡ SQL Query Studio",
    "🗺️ Geospatial Routes",
    "🔍 Raw Data Explorer"
])


# =============================================================================
# 1. OVERALL VIEW
# =============================================================================
with tab_overall:
    c1, c2 = st.columns([7, 5])
    
    with c1:
        with st.container(border=True):
            st.markdown("""
            <div class="card-title-text">📈 Ride Volume Over Time (Daily Trajectory)</div>
            <div class="card-subtitle-text">Tracking daily requests against completed trips across the month.</div>
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
                line=dict(color='#D4FF00', width=3),
                marker=dict(size=6, color='#D4FF00'),
                fill='tozeroy',
                fillcolor='rgba(212, 255, 0, 0.05)'
            ))
            fig_trend.add_trace(go.Scatter(
                x=daily_merged['Ride_Date'],
                y=daily_merged['Completed_Rides'],
                mode='lines+markers',
                name='Completed Rides',
                line=dict(color='#10B981', width=2, dash='dot'),
                marker=dict(size=4, color='#10B981')
            ))
            fig_trend = apply_theme_plot(fig_trend, height=330)
            fig_trend.update_layout(hovermode='x unified')
            st.plotly_chart(fig_trend, use_container_width=True)

            st.markdown("""
            <div class="insight-box">
                <div class="insight-row">
                    <span class="badge-insight">💡 Insight</span>
                    <span class="insight-text">Daily demand maintains a steady pace of ~3,320 rides/day, but approximately 1,260 trips fail daily due to cancellations and driver shortages.</span>
                </div>
                <div class="insight-row">
                    <span class="badge-recom">🎯 Business Action</span>
                    <span class="recom-text">Implement dynamic driver staging bonuses on high-velocity weekend dates to bridge the recurring 38% fulfillment deficit.</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with c2:
        with st.container(border=True):
            st.markdown("""
            <div class="card-title-text">🎯 Booking Status Breakdown</div>
            <div class="card-subtitle-text">Fulfillment proportions: success, cancellations, and supply gaps.</div>
            """, unsafe_allow_html=True)
            
            status_counts = filtered_df['Booking_Status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']
            
            status_palette = {
                'Success': '#10B981',
                'Canceled by Driver': '#FF3B56',
                'Canceled by Customer': '#FFB800',
                'Driver Not Found': '#5F6370'
            }
            
            fig_status = px.pie(
                status_counts,
                names='Status',
                values='Count',
                hole=0.68,
                color='Status',
                color_discrete_map=status_palette
            )
            fig_status.update_traces(
                textposition='inside',
                textinfo='percent',
                marker=dict(line=dict(color='#0B0C10', width=3))
            )
            fig_status = apply_theme_plot(fig_status, height=330)
            st.plotly_chart(fig_status, use_container_width=True)

            st.markdown("""
            <div class="insight-box">
                <div class="insight-row">
                    <span class="badge-insight">💡 Insight</span>
                    <span class="insight-text">Success rate stands at 62.09%, while driver-initiated cancellations (17.89%) constitute the single largest friction factor.</span>
                </div>
                <div class="insight-row">
                    <span class="badge-recom">🎯 Business Action</span>
                    <span class="recom-text">Penalize repeated driver-initiated cancellations and introduce 5-trip completion streaks to incentivize trip acceptance.</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Hourly Distribution & Day of Week Capsule Bar Chart
    h_col1, h_col2 = st.columns([7, 5])
    
    with h_col1:
        with st.container(border=True):
            st.markdown("""
            <div class="card-title-text">⏰ 24-Hour Demand Curve & Peak Hours</div>
            <div class="card-subtitle-text">Hourly trip requests showing morning commute (8-11 AM) and evening rush (5-9 PM).</div>
            """, unsafe_allow_html=True)
            
            hourly_split = filtered_df.groupby(['Ride_Hour', 'Booking_Status']).size().reset_index(name='Count')
            fig_hour = px.bar(
                hourly_split,
                x='Ride_Hour',
                y='Count',
                color='Booking_Status',
                color_discrete_map=status_palette,
                barmode='stack',
                labels={'Ride_Hour': 'Hour of Day (24h)', 'Count': 'Trips'}
            )
            fig_hour = apply_theme_plot(fig_hour, height=330)
            fig_hour.update_layout(xaxis=dict(tickmode='linear', tick0=0, dtick=1))
            st.plotly_chart(fig_hour, use_container_width=True)

            st.markdown("""
            <div class="insight-box">
                <div class="insight-row">
                    <span class="badge-insight">💡 Insight</span>
                    <span class="insight-text">Demand spikes sharply during the 17:00–21:00 evening commute, where 'Driver Not Found' events increase by 42%.</span>
                </div>
                <div class="insight-row">
                    <span class="badge-recom">🎯 Business Action</span>
                    <span class="recom-text">Activate automated 1.15x–1.25x micro-surge pricing during 17:00–21:00 to attract off-duty drivers onto the platform.</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with h_col2:
        with st.container(border=True):
            st.markdown("""
            <div class="card-title-text">📅 Demand Velocity by Day of Week</div>
            <div class="card-subtitle-text">Capsule bar breakdown showing weekday peak volumes vs weekends.</div>
            """, unsafe_allow_html=True)
            
            days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            dow_df = filtered_df.groupby('Day_Name').agg(
                Total_Trips=('Booking_ID', 'count')
            ).reindex(days_order).reset_index().fillna(0)
            
            max_trips = dow_df['Total_Trips'].max()
            bar_colors = ['#D4FF00' if t == max_trips else '#23252E' for t in dow_df['Total_Trips']]
            
            fig_dow = go.Figure(go.Bar(
                x=dow_df['Day_Name'].str[:3],
                y=dow_df['Total_Trips'],
                marker=dict(
                    color=bar_colors,
                    line=dict(color='rgba(255,255,255,0.08)', width=1),
                    cornerradius=12
                ),
                text=dow_df['Total_Trips'].apply(lambda x: f"{x:,}"),
                textposition='outside'
            ))
            fig_dow = apply_theme_plot(fig_dow, height=330)
            st.plotly_chart(fig_dow, use_container_width=True)

            st.markdown("""
            <div class="insight-box">
                <div class="insight-row">
                    <span class="badge-insight">💡 Insight</span>
                    <span class="insight-text">Tuesdays (16,926 rides) and Mondays (16,729) generate the highest mobility traffic, while weekend demand stabilizes at ~13,200.</span>
                </div>
                <div class="insight-row">
                    <span class="badge-recom">🎯 Business Action</span>
                    <span class="recom-text">Mandate maximum fleet readiness on Monday and Tuesday mornings to capture peak corporate commuting volumes.</span>
                </div>
            </div>
            """, unsafe_allow_html=True)


# =============================================================================
# 2. VEHICLE TYPE VIEW
# =============================================================================
with tab_veh:
    vc1, vc2 = st.columns([7, 5])
    
    with vc1:
        with st.container(border=True):
            st.markdown("""
            <div class="card-title-text">🚗 Top Vehicle Types by Ride Distance</div>
            <div class="card-subtitle-text">Average trip length (km) across all 7 vehicle tiers.</div>
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
                color_continuous_scale=[[0, '#23252E'], [0.4, '#10B981'], [1, '#D4FF00']],
                labels={'Avg_Distance': 'Avg Distance (km)', 'Vehicle_Type': 'Vehicle Category'}
            )
            fig_veh_dist.update_traces(
                texttemplate='%{text:.2f} km',
                textposition='outside',
                marker=dict(line=dict(color='rgba(255,255,255,0.08)', width=1))
            )
            fig_veh_dist = apply_theme_plot(fig_veh_dist, height=330)
            fig_veh_dist.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig_veh_dist, use_container_width=True)

            st.markdown("""
            <div class="insight-box">
                <div class="insight-row">
                    <span class="badge-insight">💡 Insight</span>
                    <span class="insight-text">Prime Sedan (15.76 km) and eBike (15.58 km) serve long commuter trips, while Auto operates strictly as short urban transit (6.24 km).</span>
                </div>
                <div class="insight-row">
                    <span class="badge-recom">🎯 Business Action</span>
                    <span class="recom-text">Reposition Auto fleets exclusively as first/last-mile metro feeder transit and market Sedan/SUV for airport/inter-suburb corridors.</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with vc2:
        with st.container(border=True):
            st.markdown("""
            <div class="card-title-text">🚕 Fleet Volume Distribution Share</div>
            <div class="card-subtitle-text">Proportional booking requests captured by each mobility tier.</div>
            """, unsafe_allow_html=True)
            
            veh_counts = filtered_df['Vehicle_Type'].value_counts().reset_index()
            veh_counts.columns = ['Vehicle_Type', 'Trips']
            
            fig_v_share = px.pie(
                veh_counts,
                names='Vehicle_Type',
                values='Trips',
                hole=0.68,
                color_discrete_sequence=['#D4FF00', '#10B981', '#00F0FF', '#FFB800', '#FF3B56', '#8E929E', '#A78BFA']
            )
            fig_v_share.update_traces(
                textposition='inside',
                textinfo='percent',
                marker=dict(line=dict(color='#0B0C10', width=3))
            )
            fig_v_share = apply_theme_plot(fig_v_share, height=330)
            st.plotly_chart(fig_v_share, use_container_width=True)

            st.markdown("""
            <div class="insight-box">
                <div class="insight-row">
                    <span class="badge-insight">💡 Insight</span>
                    <span class="insight-text">Demand is uniformly balanced across all 7 vehicle classes (~14.2% each), confirming high multi-modal customer adoption.</span>
                </div>
                <div class="insight-row">
                    <span class="badge-recom">🎯 Business Action</span>
                    <span class="recom-text">Maintain balanced driver supply quotas across 2-wheelers, autos, and cabs to prevent category cannibalization.</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Turnaround Time Performance
    with st.container(border=True):
        st.markdown("""
        <div class="card-title-text">⏱️ Turnaround Times: Vehicle Arrival (V_TAT) vs. Customer Boarding (C_TAT)</div>
        <div class="card-subtitle-text">Evaluating driver transit latency (V_TAT) against rider boarding speed (C_TAT) across fleets (in seconds).</div>
        """, unsafe_allow_html=True)
        
        tat_summary = success_records.groupby('Vehicle_Type')[['V_TAT', 'C_TAT']].mean().reset_index()
        fig_tat = px.bar(
            tat_summary,
            x='Vehicle_Type',
            y=['V_TAT', 'C_TAT'],
            barmode='group',
            color_discrete_map={'V_TAT': '#D4FF00', 'C_TAT': '#FF3B56'},
            labels={'value': 'Seconds', 'variable': 'TAT Metric', 'Vehicle_Type': 'Vehicle Category'}
        )
        fig_tat = apply_theme_plot(fig_tat, height=320)
        st.plotly_chart(fig_tat, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
            <div class="insight-row">
                <span class="badge-insight">💡 Insight</span>
                <span class="insight-text">Vehicle arrival time (V_TAT: ~170s) is double the customer boarding time (C_TAT: ~85s), driving rider wait-time dissatisfaction.</span>
            </div>
            <div class="insight-row">
                <span class="badge-recom">🎯 Business Action</span>
                <span class="recom-text">Tighten the maximum driver dispatch radius from 4 km to 2.5 km to reduce arrival latency by an estimated 35%.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# 3. REVENUE VIEW
# =============================================================================
with tab_rev:
    rc1, rc2 = st.columns([6, 6])
    
    with rc1:
        with st.container(border=True):
            st.markdown("""
            <div class="card-title-text">💳 Revenue Contribution by Payment Gateway</div>
            <div class="card-subtitle-text">Completed booking revenue split across Cash, UPI, and Card channels.</div>
            """, unsafe_allow_html=True)
            
            pm_rev = success_records.groupby('Payment_Method').agg(
                Revenue=('Booking_Value', 'sum'),
                Count=('Booking_ID', 'count')
            ).reset_index().sort_values(by='Revenue', ascending=False)
            
            fig_pm = px.pie(
                pm_rev,
                names='Payment_Method',
                values='Revenue',
                hole=0.68,
                color_discrete_sequence=['#10B981', '#D4FF00', '#00F0FF', '#A78BFA']
            )
            fig_pm.update_traces(
                textposition='inside',
                textinfo='percent',
                marker=dict(line=dict(color='#0B0C10', width=3))
            )
            fig_pm = apply_theme_plot(fig_pm, height=330)
            st.plotly_chart(fig_pm, use_container_width=True)

            st.markdown("""
            <div class="insight-box">
                <div class="insight-row">
                    <span class="badge-insight">💡 Insight</span>
                    <span class="insight-text">Physical cash remains dominant at 54.9% (₹19.26M), while UPI captures 40.4% (₹14.17M) and cards represent only 4.7%.</span>
                </div>
                <div class="insight-row">
                    <span class="badge-recom">🎯 Business Action</span>
                    <span class="recom-text">Launch a ₹20 cashback incentive for switching from Cash to UPI AutoPay to eliminate in-cab change disputes and turnaround delays.</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with rc2:
        with st.container(border=True):
            st.markdown("""
            <div class="card-title-text">👑 Top 5 Customers by Total Booking Value</div>
            <div class="card-subtitle-text">Top revenue-generating patrons and their completed trip spends.</div>
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
                color_continuous_scale=[[0, '#10B981'], [1, '#D4FF00']]
            )
            fig_top_c.update_traces(
                texttemplate='₹%{text:,}',
                textposition='outside',
                marker=dict(line=dict(color='rgba(255,255,255,0.08)', width=1))
            )
            fig_top_c = apply_theme_plot(fig_top_c, height=330)
            fig_top_c.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig_top_c, use_container_width=True)

            st.markdown("""
            <div class="insight-box">
                <div class="insight-row">
                    <span class="badge-insight">💡 Insight</span>
                    <span class="insight-text">Top power riders generate up to ₹6,019 over premium long-distance trips without recording any cancellation incidents.</span>
                </div>
                <div class="insight-row">
                    <span class="badge-recom">🎯 Business Action</span>
                    <span class="recom-text">Enroll top 5% revenue riders into an 'OLA Elite Pass' tier providing zero surge caps and priority vehicle allocation.</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Daily Distance & Revenue Profile
    with st.container(border=True):
        st.markdown("""
        <div class="card-title-text">📍 Ride Distance Distribution Per Day (Daily Fleet Mileage vs Mean Trip KM)</div>
        <div class="card-subtitle-text">Tracking aggregate fleet kilometers and average trip length across the month.</div>
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
            marker=dict(color='#23252E', line=dict(color='#D4FF00', width=1))
        ))
        fig_dual.add_trace(go.Scatter(
            x=daily_dist['Ride_Date'],
            y=daily_dist['Avg_Km'],
            name='Avg Trip Km',
            yaxis='y2',
            line=dict(color='#D4FF00', width=3)
        ))
        fig_dual = apply_theme_plot(fig_dual, height=320)
        fig_dual.update_layout(
            yaxis=dict(title="Total Fleet Distance (km)"),
            yaxis2=dict(title="Average Distance (km)", overlaying='y', side='right', showgrid=False)
        )
        st.plotly_chart(fig_dual, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
            <div class="insight-row">
                <span class="badge-insight">💡 Insight</span>
                <span class="insight-text">Daily fleet distance consistently logs 32,000–35,000 km with a remarkably steady trip length mean of 15.2 km.</span>
            </div>
            <div class="insight-row">
                <span class="badge-recom">🎯 Business Action</span>
                <span class="recom-text">Structure driver fuel/EV recharge subsidies tied to completing 120+ km per shift to sustain fleet uptime.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# 4. CANCELLATION VIEW
# =============================================================================
with tab_canc:
    canc_c1, canc_c2 = st.columns(2)
    
    with canc_c1:
        with st.container(border=True):
            st.markdown("""
            <div class="card-title-text">👤 Cancelled Rides Reasons (Customer)</div>
            <div class="card-subtitle-text">Root cause analysis behind customer-initiated cancellations (10,499 Rides).</div>
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
                color_continuous_scale=[[0, '#23252E'], [1, '#FFB800']]
            )
            fig_cr.update_traces(texttemplate='%{text:,}', textposition='outside')
            fig_cr = apply_theme_plot(fig_cr, height=310)
            fig_cr.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig_cr, use_container_width=True)

            st.markdown("""
            <div class="insight-box">
                <div class="insight-row">
                    <span class="badge-insight">💡 Insight</span>
                    <span class="insight-text">30.2% of customer cancellations (3,175 rides) occur because the driver is stationary or moving away from pickup.</span>
                </div>
                <div class="insight-row">
                    <span class="badge-recom">🎯 Business Action</span>
                    <span class="recom-text">Deploy automated GPS telemetry monitors that trigger instant ride re-dispatch if a driver shows no movement for 180 seconds.</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with canc_c2:
        with st.container(border=True):
            st.markdown("""
            <div class="card-title-text">🚗 Cancelled Rides Reasons (Drivers)</div>
            <div class="card-subtitle-text">Root cause analysis behind driver-initiated cancellations (18,434 Rides).</div>
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
                color_continuous_scale=[[0, '#23252E'], [1, '#FF3B56']]
            )
            fig_dr.update_traces(texttemplate='%{text:,}', textposition='outside')
            fig_dr = apply_theme_plot(fig_dr, height=310)
            fig_dr.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig_dr, use_container_width=True)

            st.markdown("""
            <div class="insight-box">
                <div class="insight-row">
                    <span class="badge-insight">💡 Insight</span>
                    <span class="insight-text">35.5% of driver cancellations (6,542 rides) cite 'Personal & Car related issue', signaling acute maintenance and fatigue challenges.</span>
                </div>
                <div class="insight-row">
                    <span class="badge-recom">🎯 Business Action</span>
                    <span class="recom-text">Partner with quick-service pit stop centers for express vehicle diagnostics and enforce mandatory fatigue breaks after 6 active hours.</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Incomplete Rides Breakdown
    with st.container(border=True):
        st.markdown("""
        <div class="card-title-text">⚠️ Incomplete Rides Breakdown (3,926 Trips Terminated Mid-Journey)</div>
        <div class="card-subtitle-text">Distribution of early drop-offs caused by customer demand, vehicle breakdown, and external issues.</div>
        """, unsafe_allow_html=True)
        
        inc_reasons = filtered_df[filtered_df['Incomplete_Rides'] == 'Yes']['Incomplete_Rides_Reason'].value_counts().reset_index()
        inc_reasons.columns = ['Reason', 'Count']
        
        in1, in2 = st.columns([5, 7])
        with in1:
            fig_inc_pie = px.pie(
                inc_reasons,
                names='Reason',
                values='Count',
                hole=0.68,
                color_discrete_sequence=['#FF3B56', '#FFB800', '#D4FF00']
            )
            fig_inc_pie.update_traces(
                textposition='inside',
                textinfo='percent',
                marker=dict(line=dict(color='#0B0C10', width=3))
            )
            fig_inc_pie = apply_theme_plot(fig_inc_pie, height=280)
            st.plotly_chart(fig_inc_pie, use_container_width=True)
            
        with in2:
            st.markdown("""
            <div style="background: #0E0F14; border: 1px solid rgba(255, 59, 86, 0.25); border-left: 4px solid #FF3B56; border-radius: 12px; padding: 18px; margin-top: 15px;">
                <h5 style="color: #FF3B56; margin: 0 0 8px 0; font-size: 0.95rem;">Impact of Mid-Trip Terminations</h5>
                <p style="color: #CBD5E1; font-size: 0.85rem; line-height: 1.6; margin: 0;">
                    • <b>Customer Demand (40.78% / 1,601 rides):</b> Passenger requested early exit due to severe traffic gridlock.<br>
                    • <b>Vehicle Breakdown (40.52% / 1,591 rides):</b> Engine faults, tire punctures, and battery depletion in eBikes.<br>
                    • <b>Other Issues (18.70% / 734 rides):</b> Route obstruction, bad weather, or fare payment disputes.
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="insight-box">
            <div class="insight-row">
                <span class="badge-insight">💡 Insight</span>
                <span class="insight-text">Vehicle breakdown caused 1,591 mid-trip trip abortions (40.52%), creating severe customer dissatisfaction and safety liability.</span>
            </div>
            <div class="insight-row">
                <span class="badge-recom">🎯 Business Action</span>
                <span class="recom-text">Mandate weekly vehicle fitness self-checks in the driver app and provide instant pro-rated refunds for passengers facing breakdowns.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# 5. RATINGS VIEW
# =============================================================================
with tab_rat:
    rat1, rat2 = st.columns(2)
    
    with rat1:
        with st.container(border=True):
            st.markdown("""
            <div class="card-title-text">⭐ Driver Ratings Distribution</div>
            <div class="card-subtitle-text">Scores given by passengers evaluating driver behavior and trip comfort (Citywide Avg: 4.00 / 5).</div>
            """, unsafe_allow_html=True)
            
            fig_d_hist = px.histogram(
                success_records,
                x='Driver_Ratings',
                nbins=20,
                color_discrete_sequence=['#D4FF00']
            )
            fig_d_hist = apply_theme_plot(fig_d_hist, height=290)
            fig_d_hist.update_layout(xaxis_title="Driver Rating Score", yaxis_title="Number of Trips")
            st.plotly_chart(fig_d_hist, use_container_width=True)

            st.markdown("""
            <div class="insight-box">
                <div class="insight-row">
                    <span class="badge-insight">💡 Insight</span>
                    <span class="insight-text">Driver ratings center tightly around 4.00, with no records below 3.0, indicating baseline service satisfaction.</span>
                </div>
                <div class="insight-row">
                    <span class="badge-recom">🎯 Business Action</span>
                    <span class="recom-text">Reward drivers maintaining ratings above 4.7 with preferred access to high-value airport pickup queues.</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with rat2:
        with st.container(border=True):
            st.markdown("""
            <div class="card-title-text">⭐ Customer Ratings Distribution</div>
            <div class="card-subtitle-text">Scores given by drivers evaluating rider punctuality and conduct (Citywide Avg: 4.00 / 5).</div>
            """, unsafe_allow_html=True)
            
            fig_c_hist = px.histogram(
                success_records,
                x='Customer_Rating',
                nbins=20,
                color_discrete_sequence=['#10B981']
            )
            fig_c_hist = apply_theme_plot(fig_c_hist, height=290)
            fig_c_hist.update_layout(xaxis_title="Customer Rating Score", yaxis_title="Number of Trips")
            st.plotly_chart(fig_c_hist, use_container_width=True)

            st.markdown("""
            <div class="insight-box">
                <div class="insight-row">
                    <span class="badge-insight">💡 Insight</span>
                    <span class="insight-text">Customer ratings mirror driver ratings at an average of 4.00, demonstrating mutual ecosystem trust.</span>
                </div>
                <div class="insight-row">
                    <span class="badge-recom">🎯 Business Action</span>
                    <span class="recom-text">Provide priority pickup ETA discounts to riders who consistently maintain a 4.5+ star rating.</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Cross-Fleet Rating Parity
    with st.container(border=True):
        st.markdown("""
        <div class="card-title-text">⚖️ Customer vs. Driver Ratings by Vehicle Category</div>
        <div class="card-subtitle-text">Comparing passenger and driver ratings across the 7 fleet categories to identify satisfaction gaps.</div>
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
            color_discrete_map={'Customer_Rating': '#D4FF00', 'Driver_Rating': '#10B981'}
        )
        fig_r_comp = apply_theme_plot(fig_r_comp, height=320)
        fig_r_comp.update_layout(yaxis=dict(range=[3.5, 4.3], title="Rating (Out of 5)"))
        st.plotly_chart(fig_r_comp, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
            <div class="insight-row">
                <span class="badge-insight">💡 Insight</span>
                <span class="insight-text">Rating parity is exceptionally stable across all vehicle types (3.99 to 4.01), showing uniform quality regardless of vehicle tier.</span>
            </div>
            <div class="insight-row">
                <span class="badge-recom">🎯 Business Action</span>
                <span class="recom-text">Maintain current vehicle onboarding quality benchmarks and expand premium Prime Plus perks to raise satisfaction toward 4.5.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# 6. SQL QUERY STUDIO & WORKBENCH
# =============================================================================
with tab_sql:
    sql_tab_pre, sql_tab_custom = st.tabs(["📋 Predefined Questions (1 to 10)", "✍️ Live SQL Terminal"])
    
    with sql_tab_pre:
        query_keys = list(PREDEFINED_SQL_QUERIES.keys())
        chosen_q = st.selectbox("🎯 Select Project SQL Question to Inspect & Run:", options=query_keys)
        
        q_data = PREDEFINED_SQL_QUERIES[chosen_q]
        
        with st.container(border=True):
            st.markdown(f"""
            <div style="color: #D4FF00; font-size: 0.75rem; font-weight: 800; text-transform: uppercase;">Question #{q_data['id']}</div>
            <div style="color: #FFFFFF; font-size: 1.1rem; font-weight: 700; margin: 4px 0 8px 0;">{q_data['question']}</div>
            <div style="color: #8E929E; font-size: 0.85rem;">{q_data['description']}</div>
            """, unsafe_allow_html=True)
            
            st.markdown("##### 📝 SQL Statement:")
            st.code(q_data['sql'], language="sql")
            
            c_left, c_right = st.columns([8, 4])
            with c_right:
                st.markdown(f"""
                <div style="background: #0E0F14; border: 1px solid rgba(212,255,0,0.25); border-radius: 12px; padding: 16px; font-size: 0.82rem; line-height: 1.6; color: #E2E8F0;">
                    <b style="color: #D4FF00;">Expected Result:</b><br>{q_data['expected_result']}
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
                                <span style="background: rgba(16, 185, 129, 0.15); color: #10B981; border: 1px solid rgba(16, 185, 129, 0.3); padding: 4px 12px; border-radius: 20px; font-size: 0.76rem; font-weight: 700;">
                                    ✓ Returned {row_cnt:,} rows
                                </span>
                                <span style="background: rgba(212, 255, 0, 0.15); color: #D4FF00; border: 1px solid rgba(212, 255, 0, 0.3); padding: 4px 12px; border-radius: 20px; font-size: 0.76rem; font-weight: 700;">
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
        with st.container(border=True):
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
# 7. GEOSPATIAL & ROUTE FLOW
# =============================================================================
with tab_geo:
    g1, g2 = st.columns(2)
    
    with g1:
        with st.container(border=True):
            st.markdown("""
            <div class="card-title-text">📍 Top 10 Origin Nodes (Highest Ride Requests)</div>
            <div class="card-subtitle-text">Urban origins generating the largest volume of commuter dispatch requests.</div>
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
                color_continuous_scale=[[0, '#1B1D23'], [1, '#D4FF00']]
            )
            fig_origin.update_traces(textposition='outside')
            fig_origin = apply_theme_plot(fig_origin, height=340)
            fig_origin.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig_origin, use_container_width=True)

            st.markdown("""
            <div class="insight-box">
                <div class="insight-row">
                    <span class="badge-insight">💡 Insight</span>
                    <span class="insight-text">Banashankari (2,201 requests), Yeshwanthpur (2,139), and RT Nagar (2,135) generate the highest origin passenger flow.</span>
                </div>
                <div class="insight-row">
                    <span class="badge-recom">🎯 Business Action</span>
                    <span class="recom-text">Establish dedicated OLA driver physical parking stands and rapid charging kiosks near Banashankari and Yeshwanthpur metro junctions.</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with g2:
        with st.container(border=True):
            st.markdown("""
            <div class="card-title-text">🏁 Top 10 Destination Hubs (Highest Traffic Flow)</div>
            <div class="card-subtitle-text">High-inflow commercial and residential destinations attracting daily arrivals.</div>
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
                color_continuous_scale=[[0, '#1B1D23'], [1, '#10B981']]
            )
            fig_dest.update_traces(textposition='outside')
            fig_dest = apply_theme_plot(fig_dest, height=340)
            fig_dest.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig_dest, use_container_width=True)

            st.markdown("""
            <div class="insight-box">
                <div class="insight-row">
                    <span class="badge-insight">💡 Insight</span>
                    <span class="insight-text">Drop-off destinations match origin volumes closely, demonstrating high bidirectional commuter travel across IT and commercial sectors.</span>
                </div>
                <div class="insight-row">
                    <span class="badge-recom">🎯 Business Action</span>
                    <span class="recom-text">Queue back-to-back onward bookings for drivers completing trips at these hubs to minimize deadhead return mileage.</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Top O-D Route Corridors
    with st.container(border=True):
        st.markdown("""
        <div class="card-title-text">🔁 High-Traffic Route Corridors (Origin ➡️ Destination)</div>
        <div class="card-subtitle-text">Most frequently travelled point-to-point transit pairs across Bengaluru.</div>
        """, unsafe_allow_html=True)
        
        route_traffic = filtered_df.groupby(['Pickup_Location', 'Drop_Location']).agg(
            Total_Trips=('Booking_ID', 'count'),
            Completed=('Booking_Status', lambda x: (x == 'Success').sum()),
            Total_Revenue=('Booking_Value', lambda x: x[filtered_df.loc[x.index, 'Booking_Status'] == 'Success'].sum())
        ).reset_index().sort_values(by='Total_Trips', ascending=False).head(10)
        
        st.dataframe(route_traffic, use_container_width=True)


# =============================================================================
# 8. RAW DATA EXPLORER
# =============================================================================
with tab_raw:
    with st.container(border=True):
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
            <div class="card-title-text">🔍 Raw Data Explorer & Export Engine</div>
            <span style="color: #10B981; font-weight: 700; font-size: 0.82rem;">{len(filtered_df):,} Records in Active Scope</span>
        </div>
        """, unsafe_allow_html=True)
        
        col_filter_choice = st.multiselect(
            "Select Fields to Display:",
            options=filtered_df.columns.tolist(),
            default=['Booking_ID', 'Ride_Date', 'Time_Str', 'Booking_Status', 'Customer_ID', 
                     'Vehicle_Type', 'Pickup_Location', 'Drop_Location', 'Booking_Value', 'Ride_Distance']
        )
        
        st.dataframe(filtered_df[col_filter_choice].head(1000), use_container_width=True)
        st.caption("Displaying preview of first 1,000 records. Download full filtered subset below.")
        
        raw_csv = filtered_df[col_filter_choice].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Filtered Subset (CSV)",
            data=raw_csv,
            file_name="ola_filtered_export.csv",
            mime="text/csv"
        )
