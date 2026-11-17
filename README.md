# 🚖 OLA Ride Insights - Mobility & Ride-Sharing Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.63-FF4B4B.svg)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/SQLite-3.0-003B57.svg)](https://www.sqlite.org/)
[![PowerBI](https://img.shields.io/badge/Power_BI-Desktop-F2C811.svg)](https://powerbi.microsoft.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An enterprise-grade business intelligence and data analytics platform built for **OLA Ride Insights**. This project explores **103,024 ride bookings** across Bengaluru (July 2024), extracting actionable mobility intelligence to optimize driver allocation, reduce trip cancellations, analyze revenue channels, and enhance passenger satisfaction.

---

## 📌 Table of Contents
1. [Project Overview & Problem Statement](#-project-overview--problem-statement)
2. [Key Skills & Technologies](#-key-skills--technologies)
3. [Dataset Architecture & Preprocessing](#-dataset-architecture--preprocessing)
4. [SQL Questions & Verifiable Results (1 to 10)](#-sql-questions--verifiable-results-1-to-10)
5. [Power BI Dashboard Views (5 Segregated Views)](#-power-bi-dashboard-views)
6. [Interactive Streamlit Application](#-interactive-streamlit-application)
7. [Business Use Cases & Strategic Playbook](#-business-use-cases--strategic-playbook)
8. [Project File Structure](#-project-file-structure)
9. [How to Run the Project](#-how-to-run-the-project)

---

## 📖 Project Overview & Problem Statement

Urban mobility platforms like **OLA** process millions of daily ride requests. However, converting complex telemetry and transactional records into strategic decisions presents challenges:
- **Supply-Demand Mismatch:** Localized shortages resulting in *"Driver Not Found"* events.
- **Trip Attrition:** Driver and customer cancellations causing lost Gross Merchandise Value (GMV).
- **Payment Inefficiencies:** High dependency on physical cash settlements causing turnaround delays.

This project delivers:
- **Cleaned & Feature-Engineered Dataset:** SQLite database and CSV files indexed for millisecond queries.
- **Automated SQL Query Suite:** Solutions for all 10 project SQL questions with documented business interpretations.
- **Power BI Dashboard Models:** Complete DAX formulas and multi-page layout architecture across 5 segregated views.
- **Streamlit Web Application:** Interactive dashboard replicating the Power BI visual suite, live SQL query console, and raw data explorer.

---

## 🛠️ Key Skills & Technologies

- **Data Wrangling & Pipeline:** Python (`pandas`, `numpy`, `openpyxl`)
- **Database Engine & Indexing:** `SQLite3`, `SQLAlchemy`, B-Tree Indexing
- **SQL Analysis:** Aggregations, Window Functions, Filtering, Subqueries, Conditional Logic (`CASE WHEN`)
- **Business Intelligence & Dashboards:** Power BI Desktop (DAX measures, Calculated Columns, Drilldowns)
- **Interactive Web Application:** `Streamlit`, `Plotly Express`, `Plotly Graph Objects`
- **Exploratory Data Analysis (EDA):** `seaborn`, `matplotlib`, Jupyter Notebooks

---

## 📊 Dataset Architecture & Preprocessing

The primary dataset (`OLA_DataSet.xlsx`, Sheet: `July`) contains **103,024 ride bookings**:

| Metric | Raw Dataset Count | Percentage |
| :--- | :--- | :--- |
| **Total Booking Requests** | 103,024 | 100.0% |
| **Successful Completed Rides** | 63,967 | 62.09% |
| **Canceled by Driver** | 18,434 | 17.89% |
| **Canceled by Customer** | 10,499 | 10.19% |
| **Driver Not Found (Unfulfilled)**| 10,124 | 9.83% |
| **Gross Completed Revenue** | ₹35,080,467 | ~₹3.51 Crores |
| **Average Booking Fare** | ₹548.42 | - |
| **Pickup / Drop Zones** | 50 Bangalore Nodes | - |

### Data Cleaning Highlights:
1. Standardized `Date` and `Time` into timestamps, extracted `Ride_Hour`, `Day_Name`, `Day_Of_Week`, `Is_Weekend`, and `Time_Of_Day` buckets.
2. Verified that nulls in `V_TAT`, `C_TAT`, `Payment_Method`, and ratings align with unfulfilled/cancelled rides.
3. Indexed SQLite tables on `Booking_Status`, `Vehicle_Type`, `Payment_Method`, and `Customer_ID`.

---

## 💻 SQL Questions & Verifiable Results (1 to 10)

All queries are documented in [`sql/ola_sql_queries.sql`](sql/ola_sql_queries.sql) and can be executed via `python sql_runner.py`:

### 1. Retrieve all successful bookings
```sql
SELECT Booking_ID, Ride_Date, Customer_ID, Vehicle_Type, 
       Pickup_Location, Drop_Location, Booking_Value, Ride_Distance, Payment_Method
FROM rides 
WHERE Booking_Status = 'Success';
```
- **Result:** **63,967 completed bookings** (62.09% of total volume).

---

### 2. Find the average ride distance for each vehicle type
```sql
SELECT Vehicle_Type, 
       ROUND(AVG(Ride_Distance), 2) AS Avg_Ride_Distance_KM,
       COUNT(*) AS Total_Trips
FROM rides 
GROUP BY Vehicle_Type 
ORDER BY Avg_Ride_Distance_KM DESC;
```
- **Result:**
  - `Prime Sedan`: **15.76 km** (14,877 trips)
  - `eBike`: **15.58 km** (14,816 trips)
  - `Bike`: **15.53 km** (14,662 trips)
  - `Mini`: **15.51 km** (14,552 trips)
  - `Prime Plus`: **15.45 km** (14,707 trips)
  - `Prime SUV`: **15.27 km** (14,655 trips)
  - `Auto`: **6.24 km** (14,755 trips) — *Short-distance urban micro-mobility.*

---

### 3. Get the total number of cancelled rides by customers
```sql
SELECT COUNT(*) AS Total_Cancelled_Rides_By_Customers,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rides), 2) AS Cancellation_Pct
FROM rides 
WHERE Booking_Status = 'Canceled by Customer';
```
- **Result:** **10,499 cancelled rides** (10.19% of all bookings).
- **Top Root Cause:** *"Driver is not moving towards pickup location"* (3,175 / 30.24%).

---

### 4. List the top 5 customers who booked the highest number of rides
```sql
SELECT Customer_ID, 
       COUNT(Booking_ID) AS Total_Bookings,
       SUM(CASE WHEN Booking_Status = 'Success' THEN 1 ELSE 0 END) AS Successful_Bookings,
       SUM(CASE WHEN Booking_Status = 'Success' THEN Booking_Value ELSE 0 END) AS Total_Spent_INR
FROM rides 
GROUP BY Customer_ID 
ORDER BY Total_Bookings DESC, Total_Spent_INR DESC 
LIMIT 5;
```
- **Result:**
  1. `CID954071`: 5 bookings (3 successful, ₹1,796 spent)
  2. `CID836942`: 4 bookings (4 successful, ₹6,019 spent)
  3. `CID387617`: 4 bookings (3 successful, ₹3,529 spent)
  4. `CID635963`: 4 bookings (4 successful, ₹2,841 spent)
  5. `CID309168`: 4 bookings (1 successful, ₹2,226 spent)

---

### 5. Get the number of rides cancelled by drivers due to personal and car-related issues
```sql
SELECT COUNT(*) AS Cancelled_Due_To_Personal_And_Car_Issues,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rides WHERE Booking_Status = 'Canceled by Driver'), 2) AS Driver_Cancellation_Share
FROM rides 
WHERE Canceled_Rides_by_Driver = 'Personal & Car related issue';
```
- **Result:** **6,542 rides** (35.49% of all 18,434 driver cancellations).

---

### 6. Find the maximum and minimum driver ratings for Prime Sedan bookings
```sql
SELECT Vehicle_Type,
       MAX(Driver_Ratings) AS Max_Driver_Rating, 
       MIN(Driver_Ratings) AS Min_Driver_Rating,
       ROUND(AVG(Driver_Ratings), 2) AS Avg_Driver_Rating
FROM rides 
WHERE Vehicle_Type = 'Prime Sedan' AND Driver_Ratings IS NOT NULL;
```
- **Result:** Max Rating = **5.0**, Min Rating = **3.0**, Average Rating = **3.99** (across 9,379 rated trips).

---

### 7. Retrieve all rides where payment was made using UPI
```sql
SELECT Booking_ID, Ride_Date, Customer_ID, Vehicle_Type, Booking_Value, Ride_Distance
FROM rides 
WHERE Payment_Method = 'UPI';
```
- **Result:** **25,881 completed rides** generating **₹14,168,436** in revenue (Avg ₹547.45 per ride).

---

### 8. Find the average customer rating per vehicle type
```sql
SELECT Vehicle_Type, 
       ROUND(AVG(Customer_Rating), 2) AS Avg_Customer_Rating,
       ROUND(AVG(Driver_Ratings), 2) AS Avg_Driver_Rating
FROM rides 
WHERE Customer_Rating IS NOT NULL 
GROUP BY Vehicle_Type 
ORDER BY Avg_Customer_Rating DESC;
```
- **Result:**
  - `Prime Plus`: 4.01
  - `Auto`: 4.00
  - `Mini`: 4.00
  - `Prime SUV`: 4.00
  - `Prime Sedan`: 4.00
  - `Bike`: 3.99
  - `eBike`: 3.99

---

### 9. Calculate the total booking value of rides completed successfully
```sql
SELECT SUM(Booking_Value) AS Total_Successful_Booking_Value_INR,
       COUNT(*) AS Total_Successful_Rides,
       ROUND(AVG(Booking_Value), 2) AS Avg_Booking_Value_INR
FROM rides 
WHERE Booking_Status = 'Success';
```
- **Result:** **₹35,080,467** across 63,967 completed rides (Average: ₹548.42).

---

### 10. List all incomplete rides along with the reason
```sql
SELECT Incomplete_Rides_Reason, 
       COUNT(*) AS Total_Incomplete_Rides,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rides WHERE Incomplete_Rides = 'Yes'), 2) AS Pct_Share
FROM rides 
WHERE Incomplete_Rides = 'Yes' 
GROUP BY Incomplete_Rides_Reason 
ORDER BY Total_Incomplete_Rides DESC;
```
- **Result:** Total **3,926 incomplete rides**:
  - `Customer Demand`: **1,601 rides** (40.78%)
  - `Vehicle Breakdown`: **1,591 rides** (40.52%)
  - `Other Issue`: **734 rides** (18.70%)

---

## 📈 Power BI Dashboard Views

The Power BI layout replicates the required 5 views with enterprise styling and DAX measures:
1. **Overall View:**
   - Ride Volume Over Time (daily booking trends & 24h hourly distribution).
   - Booking Status Breakdown (Donut chart with Success, Driver Cancelled, Customer Cancelled, Driver Not Found).
2. **Vehicle Type View:**
   - Top 5 Vehicle Types by Ride Distance.
   - Fleet Share & Turnaround Times (V_TAT vs C_TAT).
3. **Revenue View:**
   - Revenue Contribution by Payment Method (Cash: 54.9%, UPI: 40.4%, Cards: 4.7%).
   - Top 5 Customers by Total Booking Value.
   - Ride Distance Distribution Per Day.
4. **Cancellation View:**
   - Customer Cancellation Reasons (Driver stationary, Driver asked to cancel, Change of plans, AC not working).
   - Driver Cancellation Reasons (Personal/car issues, Customer issues, Coughing/sick).
   - Incomplete Rides Reasons (Breakdowns vs Customer Demand).
5. **Ratings View:**
   - Driver Ratings Distribution vs Customer Ratings Distribution.
   - Vehicle Type Satisfaction Comparison.

*For complete implementation details and DAX measures, see [`powerbi/PowerBI_Dashboard_Guide.md`](powerbi/PowerBI_Dashboard_Guide.md) and [`powerbi/power_bi_dax_measures.dax`](powerbi/power_bi_dax_measures.dax).*

---

## 🚀 Interactive Streamlit Application

The Streamlit web application (`app.py`) provides:
- **Executive KPI Strip:** Live cards for Total Bookings, Success Rate, Revenue, Avg Distance, and Cancellation Rate.
- **Interactive Power BI Replica:** 5 interactive tabs with Plotly charts and cross-filtering.
- **SQL Query Hub:** Execute any of the 10 project SQL queries with syntax highlighting and instant CSV export.
- **Custom SQL Console:** Write and execute custom SQL queries directly against the live database.
- **Geospatial & Route Analysis:** Top 10 pickup nodes, drop nodes, and origin-destination pairs.
- **Raw Data Explorer:** Filterable dataset table with CSV download.

---

## 💡 Business Use Cases & Strategic Playbook

1. **Driver Supply Rebalancing:**
   - *Issue:* 10,124 bookings (9.83%) failed due to *'Driver Not Found'*.
   - *Action:* Establish automated repositioning incentives toward top origin zones (Banashankari, Yeshwanthpur, RT Nagar, Indiranagar) during peak evening demand.
2. **Cancellation Reduction:**
   - *Issue:* 30.2% of customer cancellations stem from drivers remaining stationary.
   - *Action:* Implement live GPS movement monitors; reassign trip if driver does not move within 180 seconds.
3. **Fleet Maintenance Partnerships:**
   - *Issue:* 6,542 driver cancellations and 1,591 incomplete trips were caused by vehicle breakdowns.
   - *Action:* Partner with local repair stations near high-density hubs to offer free vehicle health checkups.
4. **Digital Settlement Acceleration:**
   - *Issue:* ₹19.26M (54.9%) is paid via cash, creating handling delays.
   - *Action:* Offer a 2-3% cashback on UPI AutoPay settlements to drive digital penetration to 75%+.

---

## 📂 Project File Structure

```
OLA Ride Insights/
├── OLA_DataSet.xlsx               # Original OLA raw workbook
├── OLA RIDE.docx                  # Project requirements specification
├── ola_rides.csv                  # Raw extracted CSV
├── ola_rides_cleaned.csv          # Preprocessed CSV with engineered features
├── ola_rides.db                   # SQLite database with indexes
├── run_app.bat                    # One-click Windows application launcher
├── app.py                         # Streamlit interactive BI application
├── sql_runner.py                  # CLI script to execute and verify all 10 SQL queries
├── requirements.txt               # Python package dependencies
├── README.md                      # Comprehensive project documentation
├── data/
│   ├── ola_rides_cleaned.csv      # Cleaned dataset
│   └── ola_rides.db               # SQLite database
├── sql/
│   └── ola_sql_queries.sql        # All 10 SQL queries with comments
├── src/
│   ├── __init__.py
│   ├── data_preprocessing.py      # ETL and feature engineering pipeline
│   └── db_manager.py              # SQLite connection and query manager
├── notebooks/
│   └── eda_analysis.ipynb         # Comprehensive EDA Jupyter Notebook
└── powerbi/
    ├── power_bi_dax_measures.dax  # Power BI DAX formulas and measures
    └── PowerBI_Dashboard_Guide.md # Step-by-step Power BI guide
```

---

## 💻 How to Run the Project

### 1. Run the Streamlit Interactive App:
```powershell
# Option A: Double-click or run the batch script
.\run_app.bat

# Option B: Run via Streamlit command
streamlit run app.py
```

### 2. Run the SQL Queries Verification CLI:
```powershell
python sql_runner.py
```

### 3. Re-run Data Preprocessing Pipeline:
```powershell
python src/data_preprocessing.py
```
