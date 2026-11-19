# OLA Ride Insights - Power BI Dashboard Architecture & Implementation Guide

This document provides complete instructions to connect, model, and build the 5-page Power BI Dashboard for the **OLA Ride Insights** project.

---

## 1. Data Source Connection Options

### Option A: Direct CSV / Excel Import (Simplest & Quickest)
1. Open **Power BI Desktop**.
2. Click **Get Data** -> **Text/CSV** (or **Excel Workbook**).
3. Select `data/ola_rides_cleaned.csv` or `OLA_DataSet.xlsx` (Sheet: `July`).
4. In Power Query Editor:
   - Verify `Date` is formatted as `Date`.
   - Verify `Booking_Value`, `Ride_Distance`, `V_TAT`, `C_TAT`, `Driver_Ratings`, `Customer_Rating` are numerical.
5. Click **Close & Apply**.

### Option B: MySQL Database Connection
1. Import `ola_rides_cleaned.csv` into your local MySQL database `ola_db` into table `rides`.
2. In Power BI, click **Get Data** -> **MySQL database**.
3. Server: `localhost:3306`, Database: `ola_db`.
4. Select DirectQuery or Import Mode.

---

## 2. Power BI Canvas Settings & Styling
- **Page Dimensions**: 16:9 (1280 x 720 px)
- **Background Color**: `#0F172A` (Slate Dark) or `#F8FAFC` (Clean White)
- **OLA Brand Colors**:
  - Primary Accent (OLA Lime/Green): `#9FE870` or `#16A34A`
  - Deep Dark (Contrast text): `#111827`
  - Secondary Accent (Electric Blue): `#3B82F6`
  - Alert / Cancellation (Coral / Amber): `#EF4444` / `#F59E0B`
  - Card Fill: `#1E293B` (for dark mode) or `#FFFFFF` (for light mode)

---

## 3. Global Slicers & Filter Pane (Common to all views)
- **Date Range Slicer**: Slider from `2024-07-01` to `2024-07-31`
- **Vehicle Type Slicer**: Multi-select dropdown (`Auto`, `Bike`, `eBike`, `Mini`, `Prime Plus`, `Prime Sedan`, `Prime SUV`)
- **Booking Status Slicer**: Dropdown (`Success`, `Canceled by Driver`, `Canceled by Customer`, `Driver Not Found`)

---

## 4. Visual Layouts by View (Exact Match to Project Requirements)

### View 1: Overall View
1. **Executive KPI Cards (Top Banner)**:
   - Total Bookings: `103,024`
   - Success Rate: `62.09%`
   - Total Revenue: `₹35.08M`
   - Total Cancellations: `28,933 (28.08%)`
2. **Visual 1: Ride Volume Over Time**:
   - Visual Type: **Line & Clustered Column Chart**
   - X-Axis: `Date` (Day level)
   - Column Values: `[Total Bookings]`
   - Line Values: `[Successful Bookings]`
   - Tooltip: Success Rate (%)
3. **Visual 2: Booking Status Breakdown**:
   - Visual Type: **Donut Chart**
   - Legend: `Booking_Status`
   - Values: `[Total Bookings]`
   - Data Labels: Category & Percentage (`Success: 62.1%`, `Canceled by Driver: 17.9%`, `Canceled by Customer: 10.2%`, `Driver Not Found: 9.8%`)

---

### View 2: Vehicle Type View
1. **Top 5 Vehicle Types by Ride Distance**:
   - Visual Type: **Clustered Bar Chart** (Horizontal)
   - Y-Axis: `Vehicle_Type`
   - X-Axis: `[Total Ride Distance]` or `[Average Ride Distance]`
   - Top N Filter: Top 5 by Ride Distance
2. **Vehicle Category Fleet Distribution**:
   - Visual Type: **Treemap** / **Stacked Column Chart**
   - Group: `Vehicle_Type`
   - Values: `[Total Bookings]` and `[Total Revenue]`
3. **Vehicle Operational Efficiency Matrix**:
   - Table / Matrix: `Vehicle_Type`, Total Bookings, Success Rate, Avg Distance, Avg Fare, Avg Rating.

---

### View 3: Revenue View
1. **KPI Cards**:
   - Total Completed Revenue: `₹35,080,467`
   - Average Booking Fare: `₹548.42`
   - Top Payment Method: `Cash (₹19.26M)` followed by `UPI (₹14.17M)`
2. **Visual 1: Revenue by Payment Method**:
   - Visual Type: **Donut / Stacked Bar Chart**
   - Legend: `Payment_Method`
   - Values: `[Total Revenue]`
   - Detail: Cash (54.9%), UPI (40.4%), Credit Card (3.7%), Debit Card (1.0%)
3. **Visual 2: Top 5 Customers by Total Booking Value**:
   - Visual Type: **Horizontal Bar Chart**
   - Y-Axis: `Customer_ID`
   - X-Axis: `[Total Revenue]`
   - Filters: Top 5 by Total Revenue
4. **Visual 3: Ride Distance Distribution Per Day**:
   - Visual Type: **Area / Line Chart**
   - X-Axis: `Date`
   - Y-Axis: `[Total Ride Distance]` & `[Average Ride Distance]`

---

### View 4: Cancellation View
1. **KPI Cards**:
   - Driver Cancellation Count: `18,434 (63.7% of cancellations)`
   - Customer Cancellation Count: `10,499 (36.3% of cancellations)`
   - Driver Not Found: `10,124`
2. **Visual 1: Cancelled Rides Reasons (Customer)**:
   - Visual Type: **Funnel / Horizontal Bar Chart**
   - Y-Axis: `Canceled_Rides_by_Customer`
   - X-Axis: `[Canceled by Customer]`
   - Breakdown: Driver not moving (30.2%), Driver asked to cancel (25.4%), Change of plans (19.8%), AC not working (14.9%), Wrong Address (9.6%)
3. **Visual 2: Cancelled Rides Reasons (Drivers)**:
   - Visual Type: **Donut / Bar Chart**
   - Y-Axis / Legend: `Canceled_Rides_by_Driver`
   - Values: `[Canceled by Driver]`
   - Breakdown: Personal & Car related issue (35.5%), Customer related issue (29.4%), Customer sick (19.8%), More than permitted people (15.3%)
4. **Visual 3: Incomplete Rides Breakdown**:
   - Breakdown of 3,926 incomplete rides by reason.

---

### View 5: Ratings View
1. **Visual 1: Driver Ratings Distribution**:
   - Visual Type: **Histogram / Column Chart**
   - X-Axis: `Driver_Ratings` (Bins: 3.0, 3.5, 4.0, 4.5, 5.0)
   - Y-Axis: `[Total Bookings]`
2. **Visual 2: Customer Ratings Distribution**:
   - Visual Type: **Histogram / Column Chart**
   - X-Axis: `Customer_Rating`
   - Y-Axis: `[Total Bookings]`
3. **Visual 3: Customer vs. Driver Ratings**:
   - Visual Type: **Scatter Chart / Grouped Bar Chart**
   - Categorization by `Vehicle_Type` comparing Avg Customer Rating vs Avg Driver Rating.

---

## 5. Embed in Streamlit Application
The Streamlit application replicates this entire interactive Power BI dashboard with Plotly charts, native filters, KPI counters, and SQL query explorers, providing the complete analytics experience!

