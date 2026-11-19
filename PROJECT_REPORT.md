# 🚖 OLA Ride Insights: End-to-End Mobility Analytics & Business Intelligence Report

| Deployment / Asset | Direct Clickable Access Link |
| :--- | :--- |
| **🌐 Live Interactive Web Application** | [https://ola-ride-insights-pravatsahu05.streamlit.app/](https://ola-ride-insights-pravatsahu05.streamlit.app/) |
| **💻 GitHub Source Code Repository** | [https://github.com/pravatsahu05/OLA-Ride-Insights](https://github.com/pravatsahu05/OLA-Ride-Insights) |

---

## 📌 Executive Summary & Project Metadata
Urban ride-hailing networks operate under volatile real-time demand patterns, traffic dynamics, and localized vehicle supply constraints. **OLA**, India's mobility giant, processes millions of transactional records capturing passenger demand, vehicle dispatch, turnaround times (TAT), driver cancellations, and ratings. Deriving actionable operational intelligence from these records is vital to prevent revenue leakage, improve fulfillment rates, and optimize driver retention.

This project delivers an end-to-end analytics platform evaluating **103,024 ride bookings** across Bengaluru throughout **July 2024**. The deliverable architecture includes:
1. **Automated ETL & Relational Data Engineering**: Standardized schema, feature-engineered datetime attributes, and indexed SQLite tables executing sub-second queries.
2. **Comprehensive SQL Analytics Suite**: Formulated, executed, and benchmarked solutions for all 10 critical operational questions.
3. **Power BI 5-View Intelligence Model**: Full suite of DAX measures and visualizations across Overall, Vehicle Type, Revenue, Cancellation, and Ratings views.
4. **Modern Streamlit Web Application**: An obsidian dark-matte and electric-neon volt executive dashboard featuring horizontal top filters, zero unclickable dead controls, dedicated insight badges, and an interactive SQL workbench.

---

## 📊 Dataset Architecture & Preprocessing Pipeline
The raw dataset (`OLA_DataSet.xlsx`, Sheet `July`) consists of **103,024 bookings** across 50 primary pickup and drop locations in Bengaluru.

### Pipeline Transformations (`src/data_preprocessing.py`)
- **Timestamp Parsing**: Converted raw date-time strings into standard ISO `YYYY-MM-DD` dates and integer hours (0–23).
- **Temporal Feature Engineering**: Added `Day_of_Week`, `Is_Weekend`, and `Time_Bucket` (Morning Rush 06:00–11:00, Afternoon 11:00–16:00, Evening Peak 16:00–21:00, Night 21:00–06:00).
- **Null Value Treatment**: Verified that nulls in `V_TAT` (Vehicle Search Time), `C_TAT` (Customer Arrival Time), ratings, and payment methods occur exclusively for unfulfilled/cancelled rides (39,057 rows), preserving genuine domain logic.
- **Relational Indexing (`src/db_manager.py`)**: Generated compound B-Tree indexes on `Booking_Status`, `Vehicle_Type`, `Payment_Method`, and `Customer_ID`.

### Core Operational KPI Summary (July 2024)
| Metric Name | Value / Volume | Operational Significance |
| :--- | :--- | :--- |
| **Total Booking Requests** | **103,024** | Cumulative passenger mobility demand in Bengaluru |
| **Successful Completed Rides** | **63,967 (62.09%)** | Revenue-generating completed journeys |
| **Canceled by Driver** | **18,434 (17.89%)** | Primary fulfillment bottleneck; largest cancellation driver |
| **Canceled by Customer** | **10,499 (10.19%)** | Pre-trip rider churn driven by wait times and driver delays |
| **Driver Not Found** | **10,124 (9.83%)** | Unmet demand caused by localized supply deficits |
| **Gross Realized Revenue** | **₹35,080,467** | Total booking revenue collected across completed rides |
| **Average Fare per Ride** | **₹548.42** | Average gross ticket yield per completed trip |
| **Average Trip Distance** | **15.22 km** (Excl. Auto: 6.24 km) | City-wide commuter travel distance |

---

## 🔍 Verified SQL Query Solutions (Questions 1 to 10)

### Question 1: Retrieve all successful bookings
```sql
SELECT * FROM rides WHERE Booking_Status = 'Success';
```
- **Result & Interpretation**: **63,967 completed bookings (62.09%)**. Establishes the baseline cohort for gross revenue analysis, customer frequency patterns, and driver performance evaluation.

### Question 2: Find the average ride distance for each vehicle type
```sql
SELECT Vehicle_Type, ROUND(AVG(Ride_Distance), 2) AS Avg_Distance, COUNT(*) AS Total_Trips
FROM rides GROUP BY Vehicle_Type ORDER BY Avg_Distance DESC;
```
- **Result & Interpretation**: Prime Sedan records the highest average distance (**15.76 km**), followed closely by eBike (**15.58 km**), Bike (**15.53 km**), Mini (**15.51 km**), Prime Plus (**15.45 km**), and Prime SUV (**15.27 km**). Auto operates strictly as short-haul urban micro-transit (**6.24 km**).

### Question 3: Get the total number of cancelled rides by customers
```sql
SELECT COUNT(*) AS Total_Cancelled_By_Customers FROM rides WHERE Booking_Status = 'Canceled by Customer';
```
- **Result & Interpretation**: **10,499 rides cancelled by customers (10.19%)**. Root cause analysis reveals **30.2%** cancelled due to *"Driver is not moving towards pickup location"* and **25.4%** due to *"Driver asked to cancel"*.

### Question 4: List the top 5 customers who booked the highest number of rides
```sql
SELECT Customer_ID, COUNT(Booking_ID) AS Total_Bookings, 
       SUM(CASE WHEN Booking_Status = 'Success' THEN 1 ELSE 0 END) AS Completed_Bookings
FROM rides GROUP BY Customer_ID ORDER BY Total_Bookings DESC LIMIT 5;
```
- **Result & Interpretation**: Top user **CID954071** logged 5 bookings (3 successful). Followed by **CID980727**, **CID969725**, **CID966929**, and **CID952434** with 4 bookings each.

### Question 5: Get the number of rides cancelled by drivers due to personal and car-related issues
```sql
SELECT COUNT(*) AS Cancelled_Personal_Car_Issues 
FROM rides WHERE Canceled_Rides_by_Driver = 'Personal & Car related issue';
```
- **Result & Interpretation**: **6,542 rides**, accounting for **35.49%** of all 18,434 driver cancellations. Signifies mechanical breakdowns and personal driver downtime as the single largest operational friction point.

### Question 6: Find the maximum and minimum driver ratings for Prime Sedan bookings
```sql
SELECT MAX(Driver_Ratings) AS Max_Rating, MIN(Driver_Ratings) AS Min_Rating, ROUND(AVG(Driver_Ratings), 2) AS Avg_Rating
FROM rides WHERE Vehicle_Type = 'Prime Sedan' AND Driver_Ratings IS NOT NULL;
```
- **Result & Interpretation**: Max Rating = **5.0**, Min Rating = **3.0**, Mean Rating = **3.99** across 9,379 rated Prime Sedan trips, demonstrating uniform quality standards.

### Question 7: Retrieve all rides where payment was made using UPI
```sql
SELECT COUNT(*) AS Total_UPI_Rides, SUM(Booking_Value) AS Total_Revenue, ROUND(AVG(Booking_Value), 2) AS Avg_Fare
FROM rides WHERE Payment_Method = 'UPI';
```
- **Result & Interpretation**: **25,881 completed rides** transacted via UPI, generating **₹14,168,436** (40.39% of total revenue) with an average ticket size of ₹547.45.

### Question 8: Find the average customer rating per vehicle type
```sql
SELECT Vehicle_Type, ROUND(AVG(Customer_Rating), 2) AS Avg_Customer_Rating
FROM rides WHERE Customer_Rating IS NOT NULL GROUP BY Vehicle_Type ORDER BY Avg_Customer_Rating DESC;
```
- **Result & Interpretation**: Customer ratings are exceptionally consistent across all fleet tiers: Prime Plus (**4.01**), Auto (**4.00**), Mini (**4.00**), Prime SUV (**4.00**), Prime Sedan (**4.00**), Bike (**3.99**), and eBike (**3.99**).

### Question 9: Calculate the total booking value of rides completed successfully
```sql
SELECT SUM(Booking_Value) AS Total_Successful_Booking_Value, COUNT(*) AS Total_Completed_Rides
FROM rides WHERE Booking_Status = 'Success';
```
- **Result & Interpretation**: Realized Gross Merchandise Value reached **₹35,080,467 (~₹3.51 Crores)** across 63,967 completed journeys, with an average booking fare of **₹548.42**.

### Question 10: List all incomplete rides along with the reason
```sql
SELECT Incomplete_Rides_Reason, COUNT(*) AS Total_Incomplete_Rides, 
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rides WHERE Incomplete_Rides = 'Yes'), 2) AS Pct_Share
FROM rides WHERE Incomplete_Rides = 'Yes' GROUP BY Incomplete_Rides_Reason ORDER BY Total_Incomplete_Rides DESC;
```
- **Result & Interpretation**: **3,926 rides** were prematurely aborted mid-transit: **Customer Demand** caused 1,601 aborts (40.78%), **Vehicle Breakdown** caused 1,591 aborts (40.52%), and **Other Issues** accounted for 734 aborts (18.70%).

---

## 📈 Power BI Architecture & 5 Segregated Views
1. **View 1: Overall View**: Macro volume line chart (24-hour diurnal curve peaking between 17:00 and 20:00) and central Booking Status Breakdown donut chart.
2. **View 2: Vehicle Type View**: Top 5 Vehicle Types by Ride Distance, fleet distribution shares, and turnaround duration comparisons (`V_TAT` vs `C_TAT`).
3. **View 3: Revenue View**: Payment Gateway distribution (Cash: 54.9%, UPI: 40.4%, Credit Card: 3.7%, Debit Card: 1.0%), Top 5 Customers by Value, and daily revenue collection trends.
4. **View 4: Cancellation View**: Side-by-side root-cause breakdown comparing Customer Cancellations against Driver Cancellations, plus mid-trip incomplete trip reasons.
5. **View 5: Ratings View**: Histogram distributions for Driver Ratings (mean 3.99) and Customer Ratings (mean 4.00) with category-level variance analysis.

---

## 💻 Streamlit Web Application Architecture
Hosted Live: **[https://ola-ride-insights-pravatsahu05.streamlit.app/](https://ola-ride-insights-pravatsahu05.streamlit.app/)**
- **Obsidian Dark & Electric Volt Aesthetic**: Styled with dark backgrounds (`#0D0F12`), glowing lime accents (`#D4FF00`), and typography engineered for data visibility.
- **Top Horizontal Filter Deck**: Removed restrictive sidebar navigations in favor of full-width horizontal controls (Date Window, Vehicle Tiers, Booking Status, Payment Gateways).
- **Standardized Insight & Action Cards**: Every chart is paired with a distinct `💡 Insight` badge and a `🎯 Business Action` card, bridging analytics directly with operational decision-making.
- **SQL Analytics Studio**: Built-in workbench allowing users to execute pre-built project queries or write ad-hoc SQL with execution timing benchmarks and CSV downloads.

---

## 🎯 Strategic Business Playbook & Actionable Recommendations
1. **Predictive Fleet Relocation (Recover ₹5.5M+ Lost GMV)**:
   - *Problem*: 10,124 requests failed due to *"Driver Not Found"* (9.83% deficit).
   - *Action*: Introduce dynamic relocation incentives before peak evening hours (17:00–21:00) directing idle drivers toward top demand hubs (Banashankari, Yeshwanthpur, Indiranagar).
2. **Automated Stationary Driver Alerts (Curtail 30.2% Customer Cancellations)**:
   - *Problem*: 3,175 customers cancelled because their assigned driver showed zero movement toward pickup.
   - *Action*: Trigger automated in-app pings if a driver remains stationary for > 180 seconds. Offer the rider an instant 1-tap re-dispatch to the next closest vehicle.
3. **Rapid Vehicle Diagnostics & Swapping Hubs (Mitigate 35.5% Driver Cancellations)**:
   - *Problem*: 6,542 driver cancellations and 1,591 incomplete trips resulted from mechanical/battery failures.
   - *Action*: Establish express pit-stop maintenance and rapid battery-swap stations across major suburban corridors to minimize downtime.
4. **UPI AutoPay Incentive Program (Convert 54.9% Cash Heavy Base)**:
   - *Problem*: ₹19.26M collected in cash creates cash-handling friction, safety risks, and boarding delays.
   - *Action*: Provide ₹25 instant cashback on riders' first 3 UPI AutoPay trips, driving digital payment penetration from 45.1% to > 70% within two quarters.
