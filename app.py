"""
=============================================================================
OLA RIDE INSIGHTS - ADVANCED INTERACTIVE ANALYTICS & BI DASHBOARD
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
# STREAMLIT CONFIGURATION & CUSTOM THEME
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="OLA Ride Insights | Mobility BI Dashboard",
    page_icon="🚖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium OLA Mobility UI
st.markdown("""
<style>
    /* Main Theme Overrides */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }
    
    .ola-brand-badge {
        display: inline-block;
        background-color: #B2D835;
        color: #0F172A;
        font-weight: 800;
        font-size: 0.85rem;
        padding: 4px 12px;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    
    .kpi-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 16px 20px;
        text-align: left;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: #B2D835;
    }
    
    .kpi-title {
        color: #94A3B8;
        font-size: 0.85rem;
        font-weight: 500;
        margin-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .kpi-value {
        color: #F8FAFC;
        font-size: 1.75rem;
        font-weight: 700;
        margin-bottom: 4px;
    }
    
    .kpi-subtext {
        font-size: 0.78rem;
        color: #64748B;
    }
    
    .kpi-highlight-green {
        color: #4ADE80;
        font-weight: 600;
    }
    
    .kpi-highlight-red {
        color: #F87171;
        font-weight: 600;
    }
    
    .sql-box {
        background: #090D16;
        border: 1px solid #1E293B;
        border-left: 4px solid #B2D835;
        border-radius: 8px;
        padding: 14px 18px;
        font-family: 'Fira Code', 'Courier New', monospace;
        font-size: 0.9rem;
        color: #E2E8F0;
        margin-bottom: 15px;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# DATA LOADING & CACHING
# -----------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_data():
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
    raw_df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()


# -----------------------------------------------------------------------------
# SIDEBAR FILTERS & BRANDING
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 20px 0;">
        <h1 style="color: #B2D835; margin: 0; font-size: 2.2rem; font-weight: 900; letter-spacing: -1px;">
            🚖 OLA <span style="color: #FFFFFF; font-weight: 300;">Insights</span>
        </h1>
        <p style="color: #94A3B8; font-size: 0.85rem; margin-top: 4px;">Mobility & Ride-Sharing Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🎛️ Global Data Filters")
    
    # Date Range Filter
    min_date = raw_df['Ride_Date'].min()
    max_date = raw_df['Ride_Date'].max()
    
    selected_dates = st.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Vehicle Type Filter
    all_vehicle_types = sorted(raw_df['Vehicle_Type'].dropna().unique().tolist())
    selected_vehicles = st.multiselect(
        "Vehicle Type",
        options=all_vehicle_types,
        default=all_vehicle_types
    )
    
    # Booking Status Filter
    all_statuses = sorted(raw_df['Booking_Status'].dropna().unique().tolist())
    selected_statuses = st.multiselect(
        "Booking Status",
        options=all_statuses,
        default=all_statuses
    )
    
    # Payment Method Filter
    payment_options = sorted(raw_df['Payment_Method'].dropna().unique().tolist())
    selected_payments = st.multiselect(
        "Payment Method (Completed)",
        options=payment_options,
        default=payment_options
    )
    
    st.markdown("---")
    st.markdown("""
    <div style="color: #64748B; font-size: 0.78rem; line-height: 1.5;">
        <b>Dataset:</b> Bengaluru Rides (July 2024)<br>
        <b>Records:</b> 103,024 Bookings<br>
        <b>Database:</b> SQLite 3 with B-Tree Indexes<br>
        <b>Author:</b> OLA Business Intelligence Team
    </div>
    """, unsafe_allow_html=True)

# Apply Filters
filtered_df = raw_df.copy()

if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
    start_d, end_d = selected_dates
    filtered_df = filtered_df[(filtered_df['Ride_Date'] >= start_d) & (filtered_df['Ride_Date'] <= end_d)]
elif isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 1:
    filtered_df = filtered_df[filtered_df['Ride_Date'] == selected_dates[0]]

if selected_vehicles:
    filtered_df = filtered_df[filtered_df['Vehicle_Type'].isin(selected_vehicles)]

if selected_statuses:
    filtered_df = filtered_df[filtered_df['Booking_Status'].isin(selected_statuses)]


# -----------------------------------------------------------------------------
# MAIN HEADER BANNER
# -----------------------------------------------------------------------------
st.markdown("""
<div class="main-header">
    <div class="ola-brand-badge">CAPSTONE PROJECT & ENTERPRISE BI</div>
    <h2 style="color: #FFFFFF; margin: 0 0 8px 0; font-weight: 800; font-size: 2rem;">
        OLA Ride Sharing Analytics & Executive Intelligence
    </h2>
    <p style="color: #94A3B8; margin: 0; font-size: 1rem; max-width: 900px; line-height: 1.6;">
        End-to-end data intelligence platform covering automated SQL queries, multi-view Power BI dashboard replicas, cancellation root-cause analytics, revenue streams, and interactive exploration.
    </p>
</div>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# TOP-LEVEL EXECUTIVE METRICS
# -----------------------------------------------------------------------------
total_bookings = len(filtered_df)
success_df = filtered_df[filtered_df['Booking_Status'] == 'Success']
successful_count = len(success_df)
success_rate = (successful_count / total_bookings * 100) if total_bookings > 0 else 0
total_rev = success_df['Booking_Value'].sum()
avg_fare = success_df['Booking_Value'].mean() if len(success_df) > 0 else 0
avg_distance = success_df['Ride_Distance'].mean() if len(success_df) > 0 else 0

canceled_customer_count = len(filtered_df[filtered_df['Booking_Status'] == 'Canceled by Customer'])
canceled_driver_count = len(filtered_df[filtered_df['Booking_Status'] == 'Canceled by Driver'])
driver_not_found_count = len(filtered_df[filtered_df['Booking_Status'] == 'Driver Not Found'])
total_canceled = canceled_customer_count + canceled_driver_count
cancel_rate = (total_canceled / total_bookings * 100) if total_bookings > 0 else 0

avg_cust_rating = success_df['Customer_Rating'].dropna().mean() if len(success_df) > 0 else 0
avg_driver_rating = success_df['Driver_Ratings'].dropna().mean() if len(success_df) > 0 else 0

c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Bookings</div>
        <div class="kpi-value">{total_bookings:,}</div>
        <div class="kpi-subtext">Across 50 Locations</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Success Rate</div>
        <div class="kpi-value">{success_rate:.1f}%</div>
        <div class="kpi-subtext"><span class="kpi-highlight-green">{successful_count:,}</span> Completed</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Gross Revenue</div>
        <div class="kpi-value">₹{total_rev/1e6:.2f}M</div>
        <div class="kpi-subtext">Avg Fare: <b>₹{avg_fare:.1f}</b></div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Avg Trip Distance</div>
        <div class="kpi-value">{avg_distance:.1f} km</div>
        <div class="kpi-subtext">Across All Fleets</div>
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Cancellation Rate</div>
        <div class="kpi-value">{cancel_rate:.1f}%</div>
        <div class="kpi-subtext"><span class="kpi-highlight-red">{total_canceled:,}</span> Canceled Trips</div>
    </div>
    """, unsafe_allow_html=True)

with c6:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Avg Ratings</div>
        <div class="kpi-value">⭐ {avg_cust_rating:.2f}</div>
        <div class="kpi-subtext">Driver: ⭐ {avg_driver_rating:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# APPLICATION TABS NAVIGATION
# -----------------------------------------------------------------------------
main_tab1, main_tab2, main_tab3, main_tab4, main_tab5 = st.tabs([
    "📊 Power BI Analytics Suite",
    "💻 SQL Query Hub & Workbench",
    "🗺️ Geospatial & Route Insights",
    "🔍 Raw Data Explorer",
    "💡 Business Recommendations"
])


# =============================================================================
# TAB 1: POWER BI ANALYTICS SUITE (WITH EXACT SEGREGATED VIEWS)
# =============================================================================
with main_tab1:
    st.markdown("### 📊 Power BI Dashboard Views")
    st.info("Interactive replication of the 5 Power BI views specified in the project document.")

    pbi_v1, pbi_v2, pbi_v3, pbi_v4, pbi_v5 = st.tabs([
        "1. Overall View",
        "2. Vehicle Type View",
        "3. Revenue View",
        "4. Cancellation View",
        "5. Ratings View"
    ])

    # -------------------------------------------------------------------------
    # 1. OVERALL VIEW
    # -------------------------------------------------------------------------
    with pbi_v1:
        st.markdown("#### 1. Overall View: Volume Over Time & Booking Status")
        
        col1, col2 = st.columns([7, 5])
        
        with col1:
            st.markdown("##### 📈 Ride Volume Over Time")
            daily_vol = filtered_df.groupby(['Ride_Date', 'Booking_Status']).size().reset_index(name='Rides')
            daily_total = filtered_df.groupby('Ride_Date').size().reset_index(name='Total_Rides')
            
            fig_trend = px.line(
                daily_total,
                x='Ride_Date',
                y='Total_Rides',
                markers=True,
                title="Daily Ride Volume Trend (July 2024)",
                labels={'Ride_Date': 'Date', 'Total_Rides': 'Bookings Count'},
                color_discrete_sequence=['#B2D835']
            )
            fig_trend.update_layout(
                template='plotly_dark',
                hovermode='x unified',
                margin=dict(l=20, r=20, t=40, b=20),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_trend, use_container_width=True)

        with col2:
            st.markdown("##### 🎯 Booking Status Breakdown")
            status_counts = filtered_df['Booking_Status'].value_counts().reset_index()
            status_counts.columns = ['Booking_Status', 'Count']
            
            color_map = {
                'Success': '#4ADE80',
                'Canceled by Driver': '#F87171',
                'Canceled by Customer': '#FB923C',
                'Driver Not Found': '#94A3B8'
            }
            
            fig_status = px.pie(
                status_counts,
                names='Booking_Status',
                values='Count',
                hole=0.55,
                color='Booking_Status',
                color_discrete_map=color_map,
                title="Booking Status Proportions"
            )
            fig_status.update_traces(textposition='inside', textinfo='percent+label')
            fig_status.update_layout(
                template='plotly_dark',
                margin=dict(l=20, r=20, t=40, b=20),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            st.plotly_chart(fig_status, use_container_width=True)

        # Hourly Distribution Heatmap / Bar
        st.markdown("##### ⏰ Hourly Ride Demand Profile")
        hourly_df = filtered_df.groupby(['Ride_Hour', 'Booking_Status']).size().reset_index(name='Count')
        fig_hour = px.bar(
            hourly_df,
            x='Ride_Hour',
            y='Count',
            color='Booking_Status',
            color_discrete_map=color_map,
            barmode='stack',
            title="Bookings by Hour of the Day (0:00 - 23:00)",
            labels={'Ride_Hour': 'Hour of Day (24h)', 'Count': 'Number of Bookings'}
        )
        fig_hour.update_layout(
            template='plotly_dark',
            margin=dict(l=20, r=20, t=40, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(tickmode='linear', tick0=0, dtick=1)
        )
        st.plotly_chart(fig_hour, use_container_width=True)

    # -------------------------------------------------------------------------
    # 2. VEHICLE TYPE VIEW
    # -------------------------------------------------------------------------
    with pbi_v2:
        st.markdown("#### 2. Vehicle Type View: Fleet & Distance Performance")
        
        vcol1, vcol2 = st.columns([7, 5])
        
        with vcol1:
            st.markdown("##### 🚗 Top Vehicle Types by Ride Distance")
            veh_dist = filtered_df.groupby('Vehicle_Type').agg(
                Total_Distance=('Ride_Distance', 'sum'),
                Avg_Distance=('Ride_Distance', 'mean'),
                Total_Trips=('Booking_ID', 'count')
            ).reset_index().sort_values(by='Avg_Distance', ascending=True)
            
            # Top 5 by distance
            top5_veh = veh_dist.sort_values(by='Total_Distance', ascending=False).head(5)
            
            fig_veh_dist = px.bar(
                veh_dist,
                y='Vehicle_Type',
                x='Avg_Distance',
                orientation='h',
                title="Average Ride Distance by Vehicle Type (km)",
                text='Avg_Distance',
                color='Avg_Distance',
                color_continuous_scale='Viridis',
                labels={'Avg_Distance': 'Avg Distance (km)', 'Vehicle_Type': 'Vehicle Type'}
            )
            fig_veh_dist.update_traces(texttemplate='%{text:.2f} km', textposition='outside')
            fig_veh_dist.update_layout(
                template='plotly_dark',
                margin=dict(l=20, r=20, t=40, b=20),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_veh_dist, use_container_width=True)

        with vcol2:
            st.markdown("##### 🚕 Fleet Share & Bookings Distribution")
            veh_counts = filtered_df['Vehicle_Type'].value_counts().reset_index()
            veh_counts.columns = ['Vehicle_Type', 'Bookings']
            
            fig_veh_share = px.pie(
                veh_counts,
                names='Vehicle_Type',
                values='Bookings',
                hole=0.45,
                title="Booking Share Across 7 Vehicle Categories"
            )
            fig_veh_share.update_layout(
                template='plotly_dark',
                margin=dict(l=20, r=20, t=40, b=20),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_veh_share, use_container_width=True)

        # Operational Turnaround Time (TAT) by Vehicle Type
        st.markdown("##### ⏱️ Vehicle & Customer Turnaround Time (TAT) Performance")
        tat_df = success_df.groupby('Vehicle_Type')[['V_TAT', 'C_TAT']].mean().reset_index()
        fig_tat = px.bar(
            tat_df,
            x='Vehicle_Type',
            y=['V_TAT', 'C_TAT'],
            barmode='group',
            title="Average Vehicle TAT vs Customer TAT by Vehicle Type (seconds)",
            labels={'value': 'Average Time (seconds)', 'variable': 'TAT Metric', 'Vehicle_Type': 'Vehicle Type'},
            color_discrete_map={'V_TAT': '#38BDF8', 'C_TAT': '#F472B6'}
        )
        fig_tat.update_layout(
            template='plotly_dark',
            margin=dict(l=20, r=20, t=40, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_tat, use_container_width=True)

    # -------------------------------------------------------------------------
    # 3. REVENUE VIEW
    # -------------------------------------------------------------------------
    with pbi_v3:
        st.markdown("#### 3. Revenue View: Payment Breakdown, Top Customers & Distance Profile")
        
        rcol1, rcol2 = st.columns([6, 6])
        
        with rcol1:
            st.markdown("##### 💳 Revenue by Payment Method")
            rev_pm = success_df.groupby('Payment_Method').agg(
                Total_Revenue=('Booking_Value', 'sum'),
                Trip_Count=('Booking_ID', 'count'),
                Avg_Fare=('Booking_Value', 'mean')
            ).reset_index().sort_values(by='Total_Revenue', ascending=False)
            
            fig_pm = px.pie(
                rev_pm,
                names='Payment_Method',
                values='Total_Revenue',
                hole=0.5,
                color_discrete_sequence=['#4ADE80', '#38BDF8', '#FBBF24', '#A78BFA'],
                title="Revenue Contribution by Payment Gateway"
            )
            fig_pm.update_traces(textposition='inside', textinfo='percent+label+value')
            fig_pm.update_layout(
                template='plotly_dark',
                margin=dict(l=20, r=20, t=40, b=20),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_pm, use_container_width=True)

        with rcol2:
            st.markdown("##### 👑 Top 5 Customers by Total Booking Value")
            top_cust = success_df.groupby('Customer_ID').agg(
                Total_Spent=('Booking_Value', 'sum'),
                Completed_Rides=('Booking_ID', 'count')
            ).reset_index().sort_values(by='Total_Spent', ascending=False).head(5)
            
            fig_cust = px.bar(
                top_cust.sort_values(by='Total_Spent', ascending=True),
                y='Customer_ID',
                x='Total_Spent',
                orientation='h',
                title="Top 5 Customers by Revenue (₹)",
                text='Total_Spent',
                color='Total_Spent',
                color_continuous_scale='Tealgrn',
                labels={'Total_Spent': 'Total Revenue (INR)', 'Customer_ID': 'Customer ID'}
            )
            fig_cust.update_traces(texttemplate='₹%{text:,}', textposition='outside')
            fig_cust.update_layout(
                template='plotly_dark',
                margin=dict(l=20, r=20, t=40, b=20),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_cust, use_container_width=True)

        # Ride Distance Distribution Per Day
        st.markdown("##### 📍 Ride Distance Distribution Per Day")
        daily_dist = success_df.groupby('Ride_Date').agg(
            Total_Distance=('Ride_Distance', 'sum'),
            Avg_Distance=('Ride_Distance', 'mean'),
            Total_Revenue=('Booking_Value', 'sum')
        ).reset_index()
        
        fig_dist_day = go.Figure()
        fig_dist_day.add_trace(go.Bar(
            x=daily_dist['Ride_Date'],
            y=daily_dist['Total_Distance'],
            name='Total Distance (km)',
            marker_color='#38BDF8'
        ))
        fig_dist_day.add_trace(go.Scatter(
            x=daily_dist['Ride_Date'],
            y=daily_dist['Avg_Distance'],
            name='Avg Distance (km)',
            yaxis='y2',
            line=dict(color='#F43F5E', width=3)
        ))
        fig_dist_day.update_layout(
            template='plotly_dark',
            title="Daily Total Fleet Distance & Average Trip Length",
            xaxis=dict(title="Date"),
            yaxis=dict(title="Total Fleet Distance (km)"),
            yaxis2=dict(title="Average Distance (km)", overlaying='y', side='right'),
            legend=dict(x=0.01, y=0.99),
            margin=dict(l=20, r=20, t=40, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_dist_day, use_container_width=True)

    # -------------------------------------------------------------------------
    # 4. CANCELLATION VIEW
    # -------------------------------------------------------------------------
    with pbi_v4:
        st.markdown("#### 4. Cancellation View: Driver & Customer Attrition Analysis")
        
        ccol1, ccol2 = st.columns(2)
        
        with ccol1:
            st.markdown("##### 👤 Cancelled Rides Reasons (Customer)")
            cust_cancel = filtered_df['Canceled_Rides_by_Customer'].dropna().value_counts().reset_index()
            cust_cancel.columns = ['Reason', 'Count']
            
            fig_cust_cancel = px.bar(
                cust_cancel.sort_values(by='Count', ascending=True),
                y='Reason',
                x='Count',
                orientation='h',
                title="Customer Cancellation Root Causes (10,499 Rides)",
                text='Count',
                color='Count',
                color_continuous_scale='Reds',
                labels={'Count': 'Cancellations', 'Reason': 'Cancellation Reason'}
            )
            fig_cust_cancel.update_traces(texttemplate='%{text:,}', textposition='outside')
            fig_cust_cancel.update_layout(
                template='plotly_dark',
                margin=dict(l=20, r=20, t=40, b=20),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_cust_cancel, use_container_width=True)

        with ccol2:
            st.markdown("##### 🚗 Cancelled Rides Reasons (Drivers)")
            driver_cancel = filtered_df['Canceled_Rides_by_Driver'].dropna().value_counts().reset_index()
            driver_cancel.columns = ['Reason', 'Count']
            
            fig_driver_cancel = px.bar(
                driver_cancel.sort_values(by='Count', ascending=True),
                y='Reason',
                x='Count',
                orientation='h',
                title="Driver Cancellation Root Causes (18,434 Rides)",
                text='Count',
                color='Count',
                color_continuous_scale='Oranges',
                labels={'Count': 'Cancellations', 'Reason': 'Cancellation Reason'}
            )
            fig_driver_cancel.update_traces(texttemplate='%{text:,}', textposition='outside')
            fig_driver_cancel.update_layout(
                template='plotly_dark',
                margin=dict(l=20, r=20, t=40, b=20),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_driver_cancel, use_container_width=True)

        # Incomplete Rides Analysis
        st.markdown("##### ⚠️ Incomplete Rides Breakdown (Mid-Trip Interruptions)")
        incomp_df = filtered_df[filtered_df['Incomplete_Rides'] == 'Yes']['Incomplete_Rides_Reason'].value_counts().reset_index()
        incomp_df.columns = ['Incomplete_Reason', 'Trips']
        
        ic1, ic2 = st.columns([5, 7])
        with ic1:
            fig_inc = px.pie(
                incomp_df,
                names='Incomplete_Reason',
                values='Trips',
                hole=0.45,
                title="Incomplete Rides Distribution (3,926 Trips)",
                color_discrete_sequence=['#F43F5E', '#FB923C', '#FBBF24']
            )
            fig_inc.update_layout(
                template='plotly_dark',
                margin=dict(l=20, r=20, t=40, b=20),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_inc, use_container_width=True)
            
        with ic2:
            st.markdown("""
            <div style="background: #1E293B; border-radius: 8px; padding: 20px; border-left: 4px solid #F43F5E;">
                <h5 style="color: #F87171; margin-top: 0;">Incomplete Trip Root Causes:</h5>
                <ul style="color: #CBD5E1; line-height: 1.8;">
                    <li><b>Customer Demand (40.78% / 1,601 trips):</b> Passenger requested early drop-off due to destination change or traffic bottlenecks.</li>
                    <li><b>Vehicle Breakdown (40.52% / 1,591 trips):</b> Mechanical faults, tire punctures, battery exhaustion in e-bikes.</li>
                    <li><b>Other Issues (18.70% / 734 trips):</b> Extreme weather, blocked routes, police detours, payment disputes.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 5. RATINGS VIEW
    # -------------------------------------------------------------------------
    with pbi_v5:
        st.markdown("#### 5. Ratings View: Quality, Trust & Experience Benchmarks")
        
        rat_col1, rat_col2 = st.columns(2)
        
        with rat_col1:
            st.markdown("##### ⭐ Driver Ratings Distribution")
            fig_dr_rat = px.histogram(
                success_df,
                x='Driver_Ratings',
                nbins=20,
                title="Driver Ratings Distribution (Average: 4.00)",
                color_discrete_sequence=['#38BDF8']
            )
            fig_dr_rat.update_layout(
                template='plotly_dark',
                margin=dict(l=20, r=20, t=40, b=20),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_title="Driver Rating Score",
                yaxis_title="Trips Count"
            )
            st.plotly_chart(fig_dr_rat, use_container_width=True)

        with rat_col2:
            st.markdown("##### ⭐ Customer Ratings Distribution")
            fig_cr_rat = px.histogram(
                success_df,
                x='Customer_Rating',
                nbins=20,
                title="Customer Ratings Distribution (Average: 4.00)",
                color_discrete_sequence=['#A78BFA']
            )
            fig_cr_rat.update_layout(
                template='plotly_dark',
                margin=dict(l=20, r=20, t=40, b=20),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_title="Customer Rating Score",
                yaxis_title="Trips Count"
            )
            st.plotly_chart(fig_cr_rat, use_container_width=True)

        # Customer vs Driver Ratings Comparison by Vehicle Type
        st.markdown("##### ⚖️ Customer vs. Driver Ratings by Vehicle Type")
        rat_compare = success_df.groupby('Vehicle_Type').agg(
            Avg_Customer_Rating=('Customer_Rating', 'mean'),
            Avg_Driver_Rating=('Driver_Ratings', 'mean')
        ).reset_index()
        
        fig_compare = px.bar(
            rat_compare,
            x='Vehicle_Type',
            y=['Avg_Customer_Rating', 'Avg_Driver_Rating'],
            barmode='group',
            title="Comparison of Customer vs Driver Ratings Across Categories",
            color_discrete_map={'Avg_Customer_Rating': '#4ADE80', 'Avg_Driver_Rating': '#FBBF24'}
        )
        fig_compare.update_layout(
            template='plotly_dark',
            margin=dict(l=20, r=20, t=40, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(range=[3.5, 4.5], title="Rating Score (Out of 5)")
        )
        st.plotly_chart(fig_compare, use_container_width=True)


# =============================================================================
# TAB 2: SQL QUERY HUB & WORKBENCH
# =============================================================================
with main_tab2:
    st.markdown("### 💻 SQL Query Hub & Interactive Workbench")
    st.markdown("Select from the 10 project SQL questions or author custom queries directly against the live database.")
    
    subtab_preset, subtab_custom = st.tabs(["📋 Predefined Project Queries (1-10)", "✍️ Custom SQL Console"])
    
    with subtab_preset:
        query_options = list(PREDEFINED_SQL_QUERIES.keys())
        selected_q_name = st.selectbox("Select SQL Question to Inspect & Execute:", options=query_options)
        
        query_meta = PREDEFINED_SQL_QUERIES[selected_q_name]
        
        st.markdown(f"**Question {query_meta['id']}:** {query_meta['question']}")
        st.markdown(f"*{query_meta['description']}*")
        
        # Display SQL
        st.code(query_meta['sql'], language="sql")
        
        col_exec, col_exp = st.columns([8, 4])
        with col_exp:
            st.markdown(f"""
            <div style="background: #1E293B; padding: 14px; border-radius: 8px; border-left: 3px solid #38BDF8; font-size: 0.85rem;">
                <b>Expected Result:</b><br>{query_meta['expected_result']}
            </div>
            """, unsafe_allow_html=True)
            
        with col_exec:
            if st.button(f"▶️ Run Query {query_meta['id']}", key=f"btn_run_{query_meta['id']}"):
                with st.spinner("Executing query on SQLite..."):
                    sql_to_run = query_meta.get("count_sql") or query_meta.get("breakdown_sql") or query_meta["sql"]
                    if "LIMIT" not in sql_to_run and ("SELECT *" in sql_to_run or "SELECT Booking_ID" in sql_to_run):
                        sql_to_run = query_meta["sql"] + " LIMIT 100"
                        st.caption("ℹ️ Displaying first 100 records for performance.")
                    
                    df_res, count, ms, err = execute_query(sql_to_run)
                    if err:
                        st.error(f"SQL Error: {err}")
                    else:
                        st.success(f"Query returned {count:,} records in {ms} ms.")
                        st.dataframe(df_res, use_container_width=True)
                        
                        csv_data = df_res.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label=f"📥 Download Query {query_meta['id']} Results (CSV)",
                            data=csv_data,
                            file_name=f"ola_query_{query_meta['id']}_results.csv",
                            mime="text/csv"
                        )
                        
    with subtab_custom:
        st.markdown("##### ✍️ Run Custom SQL Against `rides` Table")
        default_custom = "SELECT Vehicle_Type, COUNT(*) as Total_Trips, ROUND(AVG(Booking_Value), 2) as Avg_Fare\nFROM rides\nWHERE Booking_Status = 'Success'\nGROUP BY Vehicle_Type\nORDER BY Total_Trips DESC;"
        user_sql = st.text_area("SQL Statement:", value=default_custom, height=120)
        
        if st.button("🚀 Execute Custom SQL", key="btn_custom_sql"):
            with st.spinner("Executing..."):
                df_cust, c_count, c_ms, c_err = execute_query(user_sql)
                if c_err:
                    st.error(f"SQL Error: {c_err}")
                else:
                    st.success(f"Executed in {c_ms} ms. Returned {c_count:,} rows.")
                    st.dataframe(df_cust, use_container_width=True)


# =============================================================================
# TAB 3: GEOSPATIAL & ROUTE INSIGHTS
# =============================================================================
with main_tab3:
    st.markdown("### 🗺️ Geospatial & Location Hotspots (Bengaluru)")
    st.markdown("Analyze demand patterns across 50 urban pick-up and drop-off nodes.")
    
    loc_col1, loc_col2 = st.columns(2)
    
    with loc_col1:
        st.markdown("##### 📍 Top 10 Pickup Locations by Demand")
        top_pickup = filtered_df['Pickup_Location'].value_counts().head(10).reset_index()
        top_pickup.columns = ['Pickup_Location', 'Demand']
        
        fig_pickup = px.bar(
            top_pickup.sort_values(by='Demand', ascending=True),
            y='Pickup_Location',
            x='Demand',
            orientation='h',
            title="Highest Origin Demand Zones",
            text='Demand',
            color='Demand',
            color_continuous_scale='Greens'
        )
        fig_pickup.update_traces(textposition='outside')
        fig_pickup.update_layout(template='plotly_dark', coloraxis_showscale=False)
        st.plotly_chart(fig_pickup, use_container_width=True)

    with loc_col2:
        st.markdown("##### 🏁 Top 10 Drop Locations by Traffic")
        top_drop = filtered_df['Drop_Location'].value_counts().head(10).reset_index()
        top_drop.columns = ['Drop_Location', 'Volume']
        
        fig_drop = px.bar(
            top_drop.sort_values(by='Volume', ascending=True),
            y='Drop_Location',
            x='Volume',
            orientation='h',
            title="Highest Destination Flow Zones",
            text='Volume',
            color='Volume',
            color_continuous_scale='Blues'
        )
        fig_drop.update_traces(textposition='outside')
        fig_drop.update_layout(template='plotly_dark', coloraxis_showscale=False)
        st.plotly_chart(fig_drop, use_container_width=True)

    # Route Origin-Destination Matrix
    st.markdown("##### 🔁 Top Route Corridors (Origin ➡️ Destination)")
    route_df = filtered_df.groupby(['Pickup_Location', 'Drop_Location']).size().reset_index(name='Trips')
    top_routes = route_df.sort_values(by='Trips', ascending=False).head(10)
    st.dataframe(top_routes, use_container_width=True)


# =============================================================================
# TAB 4: RAW DATA EXPLORER
# =============================================================================
with main_tab4:
    st.markdown("### 🔍 Raw Data Explorer & Export")
    st.markdown(f"Viewing filtered dataset containing **{len(filtered_df):,}** records.")
    
    show_cols = st.multiselect(
        "Select Columns to View:",
        options=filtered_df.columns.tolist(),
        default=['Booking_ID', 'Ride_Date', 'Time_Str', 'Booking_Status', 'Customer_ID', 
                 'Vehicle_Type', 'Pickup_Location', 'Drop_Location', 'Booking_Value', 'Ride_Distance']
    )
    
    st.dataframe(filtered_df[show_cols].head(500), use_container_width=True)
    st.caption("Showing preview of first 500 rows. Use export button below to download the full filtered set.")
    
    csv_raw = filtered_df[show_cols].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Dataset (CSV)",
        data=csv_raw,
        file_name="ola_filtered_data.csv",
        mime="text/csv"
    )


# =============================================================================
# TAB 5: BUSINESS RECOMMENDATIONS & STRATEGIC PLAYBOOK
# =============================================================================
with main_tab5:
    st.markdown("### 💡 Strategic Business Playbook & Operational Insights")
    
    st.markdown("""
    Based on the analysis of **103,024 bookings** across July 2024, here are the actionable business recommendations:
    """)
    
    rec1, rec2 = st.columns(2)
    
    with rec1:
        st.markdown("""
        <div style="background: #1E293B; border-radius: 10px; padding: 20px; border-left: 4px solid #4ADE80; margin-bottom: 20px;">
            <h4 style="color: #4ADE80; margin-top: 0;">1. Driver Allocation & Surge Pricing Optimization</h4>
            <p style="color: #CBD5E1; font-size: 0.9rem;">
                <b>Insight:</b> 10,124 bookings (9.83%) failed due to <i>'Driver Not Found'</i>, indicating acute localized supply deficits.<br>
                <b>Action:</b>
                <ul>
                    <li>Implement proactive rebalancing incentives to reposition idle drivers towards high-demand nodes (Banashankari, Yeshwanthpur, Indiranagar).</li>
                    <li>Introduce micro-surge pricing (1.1x - 1.25x) during evening rush hours (17:00 - 21:00) to incentivize driver log-ins.</li>
                </ul>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #1E293B; border-radius: 10px; padding: 20px; border-left: 4px solid #F87171; margin-bottom: 20px;">
            <h4 style="color: #F87171; margin-top: 0;">2. Mitigation of Driver Cancellations</h4>
            <p style="color: #CBD5E1; font-size: 0.9rem;">
                <b>Insight:</b> Driver cancellations accounted for 18,434 rides (17.89% of all bookings), with 35.5% citing <i>'Personal & Car related issue'</i>.<br>
                <b>Action:</b>
                <ul>
                    <li>Establish partner quick-service vehicle maintenance hubs near top density pickup hubs.</li>
                    <li>Limit penalization-free cancellations to 2 per shift, while offering completion streak bonuses.</li>
                </ul>
            </p>
        </div>
        """, unsafe_allow_html=True)

    with rec2:
        st.markdown("""
        <div style="background: #1E293B; border-radius: 10px; padding: 20px; border-left: 4px solid #38BDF8; margin-bottom: 20px;">
            <h4 style="color: #38BDF8; margin-top: 0;">3. Customer Experience & Transparent ETA</h4>
            <p style="color: #CBD5E1; font-size: 0.9rem;">
                <b>Insight:</b> 30.2% of customer cancellations were caused by <i>'Driver is not moving towards pickup location'</i>.<br>
                <b>Action:</b>
                <ul>
                    <li>Enhance GPS telemetry with live traffic-adjusted ETA updates.</li>
                    <li>Automate rerouting/reassignment if a driver remains stationary for > 3 minutes after accepting.</li>
                </ul>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #1E293B; border-radius: 10px; padding: 20px; border-left: 4px solid #FBBF24; margin-bottom: 20px;">
            <h4 style="color: #FBBF24; margin-top: 0;">4. Digital Payments & UPI Expansion</h4>
            <p style="color: #CBD5E1; font-size: 0.9rem;">
                <b>Insight:</b> Cash still represents 54.9% of completed transactions (₹19.26M), while UPI represents 40.4% (₹14.17M).<br>
                <b>Action:</b>
                <ul>
                    <li>Roll out 1-click UPI Autopay cashback discounts (2-5% off) to transition cash transactions to instant digital settlements.</li>
                    <li>Eliminates change-handling friction and reduces in-cab settlement delays.</li>
                </ul>
            </p>
        </div>
        """, unsafe_allow_html=True)
