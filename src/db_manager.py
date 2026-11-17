"""
Database Manager Module for OLA Ride Insights
Provides connection handling, predefined SQL queries from the problem statement, and custom query execution.
"""

import os
import sqlite3
import time
import pandas as pd

DB_PATH = "data/ola_rides.db" if os.path.exists("data/ola_rides.db") else "ola_rides.db"

PREDEFINED_SQL_QUERIES = {
    "1. Retrieve all successful bookings": {
        "id": 1,
        "question": "Retrieve all successful bookings:",
        "sql": """SELECT Booking_ID, Ride_Date, Time_Str AS Time, Customer_ID, Vehicle_Type, 
       Pickup_Location, Drop_Location, Booking_Value, Ride_Distance, Payment_Method
FROM rides 
WHERE Booking_Status = 'Success';""",
        "count_sql": """SELECT COUNT(*) AS Total_Successful_Bookings 
FROM rides 
WHERE Booking_Status = 'Success';""",
        "description": "Filters the dataset for all records where Booking_Status equals 'Success'.",
        "expected_result": "63,967 successful bookings out of 103,024 total bookings (62.09% success rate)."
    },
    "2. Find the average ride distance for each vehicle type": {
        "id": 2,
        "question": "Find the average ride distance for each vehicle type:",
        "sql": """SELECT Vehicle_Type, 
       ROUND(AVG(Ride_Distance), 2) AS Avg_Ride_Distance_KM,
       COUNT(*) AS Total_Rides,
       ROUND(MIN(Ride_Distance), 2) AS Min_Distance,
       ROUND(MAX(Ride_Distance), 2) AS Max_Distance
FROM rides 
GROUP BY Vehicle_Type 
ORDER BY Avg_Ride_Distance_KM DESC;""",
        "description": "Aggregates ride distance by vehicle type using AVG() and groups by Vehicle_Type.",
        "expected_result": "Sedan, eBike, Bike, Mini, Prime Plus, and Prime SUV average ~15.3-15.8 km, while Auto averages 6.24 km."
    },
    "3. Get the total number of cancelled rides by customers": {
        "id": 3,
        "question": "Get the total number of cancelled rides by customers:",
        "sql": """SELECT COUNT(*) AS Total_Cancelled_Rides_By_Customers,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rides), 2) AS Pct_Of_Total_Bookings
FROM rides 
WHERE Booking_Status = 'Canceled by Customer';""",
        "breakdown_sql": """SELECT Canceled_Rides_by_Customer AS Cancellation_Reason, 
       COUNT(*) AS Count,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rides WHERE Booking_Status = 'Canceled by Customer'), 2) AS Pct_Share
FROM rides 
WHERE Booking_Status = 'Canceled by Customer'
GROUP BY Canceled_Rides_by_Customer
ORDER BY Count DESC;""",
        "description": "Calculates the total count of customer cancellations.",
        "expected_result": "10,499 rides cancelled by customers (10.19% of all bookings)."
    },
    "4. List the top 5 customers who booked the highest number of rides": {
        "id": 4,
        "question": "List the top 5 customers who booked the highest number of rides:",
        "sql": """SELECT Customer_ID, 
       COUNT(Booking_ID) AS Total_Bookings,
       SUM(CASE WHEN Booking_Status = 'Success' THEN 1 ELSE 0 END) AS Successful_Bookings,
       SUM(CASE WHEN Booking_Status = 'Success' THEN Booking_Value ELSE 0 END) AS Total_Spent_INR
FROM rides 
GROUP BY Customer_ID 
ORDER BY Total_Bookings DESC, Total_Spent_INR DESC 
LIMIT 5;""",
        "description": "Counts bookings per Customer_ID and orders descending with LIMIT 5.",
        "expected_result": "Top customer CID954071 (5 bookings), followed by CID980727, CID969725, CID966929, CID952434 (4 bookings each)."
    },
    "5. Get the number of rides cancelled by drivers due to personal and car-related issues": {
        "id": 5,
        "question": "Get the number of rides cancelled by drivers due to personal and car-related issues:",
        "sql": """SELECT COUNT(*) AS Cancelled_Due_To_Personal_And_Car_Issues,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rides WHERE Booking_Status = 'Canceled by Driver'), 2) AS Pct_Of_Driver_Cancellations
FROM rides 
WHERE Canceled_Rides_by_Driver = 'Personal & Car related issue';""",
        "description": "Filters rides cancelled specifically for 'Personal & Car related issue'.",
        "expected_result": "6,542 rides (35.49% of all 18,434 driver cancellations)."
    },
    "6. Find the maximum and minimum driver ratings for Prime Sedan bookings": {
        "id": 6,
        "question": "Find the maximum and minimum driver ratings for Prime Sedan bookings:",
        "sql": """SELECT Vehicle_Type,
       MAX(Driver_Ratings) AS Max_Driver_Rating, 
       MIN(Driver_Ratings) AS Min_Driver_Rating,
       ROUND(AVG(Driver_Ratings), 2) AS Avg_Driver_Rating,
       COUNT(Driver_Ratings) AS Total_Rated_Rides
FROM rides 
WHERE Vehicle_Type = 'Prime Sedan' AND Driver_Ratings IS NOT NULL;""",
        "description": "Calculates MAX, MIN, and AVG Driver_Ratings for 'Prime Sedan'.",
        "expected_result": "Maximum Rating = 5.0, Minimum Rating = 3.0, Average Rating = 4.00 across 9,219 rated Prime Sedan rides."
    },
    "7. Retrieve all rides where payment was made using UPI": {
        "id": 7,
        "question": "Retrieve all rides where payment was made using UPI:",
        "sql": """SELECT Booking_ID, Ride_Date, Customer_ID, Vehicle_Type, 
       Booking_Value, Ride_Distance, Payment_Method
FROM rides 
WHERE Payment_Method = 'UPI';""",
        "count_sql": """SELECT COUNT(*) AS Total_UPI_Rides,
       SUM(Booking_Value) AS Total_UPI_Revenue_INR,
       ROUND(AVG(Booking_Value), 2) AS Avg_UPI_Fare_INR
FROM rides 
WHERE Payment_Method = 'UPI';""",
        "description": "Filters all rides where Payment_Method is 'UPI'.",
        "expected_result": "25,881 rides paid via UPI, generating ₹14,168,436 in revenue."
    },
    "8. Find the average customer rating per vehicle type": {
        "id": 8,
        "question": "Find the average customer rating per vehicle type:",
        "sql": """SELECT Vehicle_Type, 
       ROUND(AVG(Customer_Rating), 2) AS Avg_Customer_Rating,
       ROUND(AVG(Driver_Ratings), 2) AS Avg_Driver_Rating,
       COUNT(Customer_Rating) AS Total_Rated_Rides
FROM rides 
WHERE Customer_Rating IS NOT NULL 
GROUP BY Vehicle_Type 
ORDER BY Avg_Customer_Rating DESC;""",
        "description": "Computes average customer rating for each vehicle category.",
        "expected_result": "Consistently close to 4.00 across all categories (Prime Plus: 4.01, Prime Sedan: 4.00, Prime SUV: 4.00, Mini: 4.00, Auto: 4.00, eBike: 3.99, Bike: 3.99)."
    },
    "9. Calculate the total booking value of rides completed successfully": {
        "id": 9,
        "question": "Calculate the total booking value of rides completed successfully:",
        "sql": """SELECT SUM(Booking_Value) AS Total_Successful_Booking_Value_INR,
       COUNT(*) AS Total_Successful_Rides,
       ROUND(AVG(Booking_Value), 2) AS Avg_Booking_Value_INR
FROM rides 
WHERE Booking_Status = 'Success';""",
        "description": "Sums the Booking_Value column for all rows where Booking_Status = 'Success'.",
        "expected_result": "Total revenue = ₹35,080,467 across 63,967 completed rides (Average ₹548.41 per ride)."
    },
    "10. List all incomplete rides along with the reason": {
        "id": 10,
        "question": "List all incomplete rides along with the reason:",
        "sql": """SELECT Booking_ID, Ride_Date, Customer_ID, Vehicle_Type, 
       Incomplete_Rides, Incomplete_Rides_Reason, Booking_Value, Ride_Distance
FROM rides 
WHERE Incomplete_Rides = 'Yes';""",
        "breakdown_sql": """SELECT Incomplete_Rides_Reason, 
       COUNT(*) AS Total_Incomplete_Rides,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rides WHERE Incomplete_Rides = 'Yes'), 2) AS Pct_Share
FROM rides 
WHERE Incomplete_Rides = 'Yes' 
GROUP BY Incomplete_Rides_Reason 
ORDER BY Total_Incomplete_Rides DESC;""",
        "description": "Lists all rides marked as Incomplete along with the specific reason.",
        "expected_result": "3,926 incomplete rides: Customer Demand (1,601 / 40.78%), Vehicle Breakdown (1,591 / 40.52%), Other Issue (734 / 18.70%)."
    }
}

def get_connection(db_file=None):
    if db_file is None:
        db_file = DB_PATH if os.path.exists(DB_PATH) else "ola_rides.db"
    return sqlite3.connect(db_file)

def execute_query(sql, params=None, db_file=None):
    """Executes a SQL query and returns results dataframe, row count, and execution time in ms."""
    conn = get_connection(db_file)
    start_time = time.time()
    try:
        if params:
            df = pd.read_sql_query(sql, conn, params=params)
        else:
            df = pd.read_sql_query(sql, conn)
        elapsed_ms = (time.time() - start_time) * 1000.0
        return df, len(df), round(elapsed_ms, 2), None
    except Exception as e:
        return pd.DataFrame(), 0, 0, str(e)
    finally:
        conn.close()

def get_executive_kpis(db_file=None):
    """Fetches high-level executive KPIs in a single optimized query."""
    conn = get_connection(db_file)
    query = """
    SELECT 
        COUNT(*) AS Total_Bookings,
        SUM(CASE WHEN Booking_Status = 'Success' THEN 1 ELSE 0 END) AS Successful_Bookings,
        SUM(CASE WHEN Booking_Status = 'Canceled by Customer' THEN 1 ELSE 0 END) AS Canceled_Customer,
        SUM(CASE WHEN Booking_Status = 'Canceled by Driver' THEN 1 ELSE 0 END) AS Canceled_Driver,
        SUM(CASE WHEN Booking_Status = 'Driver Not Found' THEN 1 ELSE 0 END) AS Driver_Not_Found,
        SUM(CASE WHEN Booking_Status = 'Success' THEN Booking_Value ELSE 0 END) AS Total_Revenue,
        ROUND(AVG(CASE WHEN Booking_Status = 'Success' THEN Ride_Distance ELSE NULL END), 2) AS Avg_Distance,
        ROUND(AVG(Customer_Rating), 2) AS Avg_Customer_Rating,
        ROUND(AVG(Driver_Ratings), 2) AS Avg_Driver_Rating
    FROM rides;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    total = df['Total_Bookings'].iloc[0]
    success = df['Successful_Bookings'].iloc[0]
    rev = df['Total_Revenue'].iloc[0]
    
    return {
        "total_bookings": int(total),
        "successful_bookings": int(success),
        "success_rate": round(success * 100.0 / total, 2),
        "total_revenue": float(rev),
        "avg_distance": float(df['Avg_Distance'].iloc[0]),
        "canceled_customer": int(df['Canceled_Customer'].iloc[0]),
        "canceled_driver": int(df['Canceled_Driver'].iloc[0]),
        "driver_not_found": int(df['Driver_Not_Found'].iloc[0]),
        "cancellation_rate": round((df['Canceled_Customer'].iloc[0] + df['Canceled_Driver'].iloc[0]) * 100.0 / total, 2),
        "avg_customer_rating": float(df['Avg_Customer_Rating'].iloc[0]),
        "avg_driver_rating": float(df['Avg_Driver_Rating'].iloc[0])
    }
