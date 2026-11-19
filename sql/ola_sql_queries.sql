-- ==============================================================================
-- PROJECT TITLE: OLA RIDE INSIGHTS - SQL QUERIES & BUSINESS INTELLIGENCE
-- DOMAIN: Ride-Sharing & Mobility Analytics
-- DATABASE COMPATIBILITY: SQLite, MySQL 8+, PostgreSQL 12+
-- ==============================================================================

-- Create Database & Table Schema Reference
-- CREATE TABLE rides (
--     Date TIMESTAMP,
--     Time VARCHAR(20),
--     Booking_ID VARCHAR(50) PRIMARY KEY,
--     Booking_Status VARCHAR(50),
--     Customer_ID VARCHAR(50),
--     Vehicle_Type VARCHAR(50),
--     Pickup_Location VARCHAR(100),
--     Drop_Location VARCHAR(100),
--     V_TAT FLOAT,
--     C_TAT FLOAT,
--     Canceled_Rides_by_Customer VARCHAR(255),
--     Canceled_Rides_by_Driver VARCHAR(255),
--     Incomplete_Rides VARCHAR(10),
--     Incomplete_Rides_Reason VARCHAR(255),
--     Booking_Value INT,
--     Payment_Method VARCHAR(50),
--     Ride_Distance INT,
--     Driver_Ratings FLOAT,
--     Customer_Rating FLOAT,
--     Ride_Date VARCHAR(20),
--     Ride_Hour INT,
--     Day_Name VARCHAR(20),
--     Day_Of_Week INT,
--     Is_Weekend INT,
--     Time_Of_Day VARCHAR(50)
-- );

-- ------------------------------------------------------------------------------
-- QUESTION 1: Retrieve all successful bookings
-- Business Context: Essential for analyzing fulfilled trips, customer retention, and net revenue generation.
-- Expected Output: 63,967 rows
-- ------------------------------------------------------------------------------
SELECT 
    Booking_ID,
    Ride_Date,
    Time,
    Customer_ID,
    Vehicle_Type,
    Pickup_Location,
    Drop_Location,
    Booking_Value,
    Ride_Distance,
    Payment_Method
FROM rides
WHERE Booking_Status = 'Success';

-- Summary Count Verification for Question 1:
SELECT 
    COUNT(*) AS Total_Successful_Bookings,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rides), 2) AS Success_Percentage
FROM rides
WHERE Booking_Status = 'Success';


-- ------------------------------------------------------------------------------
-- QUESTION 2: Find the average ride distance for each vehicle type
-- Business Context: Determines fleet deployment strategy; e.g. short micro-trips (Auto) vs long commutes (Sedan/SUV).
-- Expected Output: 7 rows ordered by Avg_Distance descending
-- ------------------------------------------------------------------------------
SELECT 
    Vehicle_Type,
    ROUND(AVG(Ride_Distance), 2) AS Avg_Ride_Distance_KM,
    COUNT(*) AS Total_Trips,
    ROUND(MIN(Ride_Distance), 2) AS Min_Distance_KM,
    ROUND(MAX(Ride_Distance), 2) AS Max_Distance_KM
FROM rides
GROUP BY Vehicle_Type
ORDER BY Avg_Ride_Distance_KM DESC;


-- ------------------------------------------------------------------------------
-- QUESTION 3: Get the total number of cancelled rides by customers
-- Business Context: Quantifies customer attrition at the pre-trip stage and identifies booking intent loss.
-- Expected Output: 10,499 cancelled rides
-- ------------------------------------------------------------------------------
SELECT 
    COUNT(*) AS Total_Cancelled_Rides_By_Customers,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rides), 2) AS Customer_Cancellation_Rate_Pct
FROM rides
WHERE Booking_Status = 'Canceled by Customer';

-- Additional Root Cause Breakdown for Customer Cancellations:
SELECT 
    Canceled_Rides_by_Customer AS Customer_Cancellation_Reason,
    COUNT(*) AS Total_Cancellations,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rides WHERE Booking_Status = 'Canceled by Customer'), 2) AS Pct_Share
FROM rides
WHERE Booking_Status = 'Canceled by Customer'
GROUP BY Canceled_Rides_by_Customer
ORDER BY Total_Cancellations DESC;


-- ------------------------------------------------------------------------------
-- QUESTION 4: List the top 5 customers who booked the highest number of rides
-- Business Context: Identifies high-frequency power users for loyalty tiers and tailored marketing promotions.
-- Expected Output: Top 5 Customer IDs with ride counts and successful ride totals
-- ------------------------------------------------------------------------------
SELECT 
    Customer_ID,
    COUNT(Booking_ID) AS Total_Bookings,
    SUM(CASE WHEN Booking_Status = 'Success' THEN 1 ELSE 0 END) AS Successful_Bookings,
    SUM(CASE WHEN Booking_Status = 'Success' THEN Booking_Value ELSE 0 END) AS Total_Revenue_INR
FROM rides
GROUP BY Customer_ID
ORDER BY Total_Bookings DESC, Total_Revenue_INR DESC
LIMIT 5;


-- ------------------------------------------------------------------------------
-- QUESTION 5: Get the number of rides cancelled by drivers due to personal and car-related issues
-- Business Context: Helps fleet operations tackle vehicle maintenance downtime and driver availability challenges.
-- Expected Output: 6,542 rides
-- ------------------------------------------------------------------------------
SELECT 
    COUNT(*) AS Driver_Cancellations_Personal_Car_Issue,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rides WHERE Booking_Status = 'Canceled by Driver'), 2) AS Pct_Of_Driver_Cancellations
FROM rides
WHERE Canceled_Rides_by_Driver = 'Personal & Car related issue';

-- Driver Cancellation Breakdown Across All Reasons:
SELECT 
    Canceled_Rides_by_Driver AS Driver_Cancellation_Reason,
    COUNT(*) AS Total_Cancellations,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rides WHERE Booking_Status = 'Canceled by Driver'), 2) AS Pct_Share
FROM rides
WHERE Booking_Status = 'Canceled by Driver'
GROUP BY Canceled_Rides_by_Driver
ORDER BY Total_Cancellations DESC;


-- ------------------------------------------------------------------------------
-- QUESTION 6: Find the maximum and minimum driver ratings for Prime Sedan bookings
-- Business Context: Quality benchmarking for OLA's premium executive ride segment.
-- Expected Output: Max: 5.0, Min: 3.0, Avg: 4.00
-- ------------------------------------------------------------------------------
SELECT 
    Vehicle_Type,
    MAX(Driver_Ratings) AS Max_Driver_Rating,
    MIN(Driver_Ratings) AS Min_Driver_Rating,
    ROUND(AVG(Driver_Ratings), 2) AS Avg_Driver_Rating,
    COUNT(Driver_Ratings) AS Total_Rated_Trips
FROM rides
WHERE Vehicle_Type = 'Prime Sedan' AND Driver_Ratings IS NOT NULL;


-- ------------------------------------------------------------------------------
-- QUESTION 7: Retrieve all rides where payment was made using UPI
-- Business Context: Digital payment adoption tracking for fintech integrations and instant settlement pipelines.
-- Expected Output: 25,881 rides
-- ------------------------------------------------------------------------------
SELECT 
    Booking_ID,
    Ride_Date,
    Time,
    Customer_ID,
    Vehicle_Type,
    Booking_Value,
    Ride_Distance,
    Payment_Method
FROM rides
WHERE Payment_Method = 'UPI';

-- Summary Revenue Metrics for UPI Payments:
SELECT 
    Payment_Method,
    COUNT(*) AS Total_Transactions,
    SUM(Booking_Value) AS Total_Revenue_INR,
    ROUND(AVG(Booking_Value), 2) AS Avg_Transaction_Value_INR
FROM rides
WHERE Payment_Method = 'UPI';


-- ------------------------------------------------------------------------------
-- QUESTION 8: Find the average customer rating per vehicle type
-- Business Context: Evaluates customer satisfaction across different vehicle tiers (economy vs premium).
-- Expected Output: 7 rows with vehicle types and avg customer ratings
-- ------------------------------------------------------------------------------
SELECT 
    Vehicle_Type,
    ROUND(AVG(Customer_Rating), 2) AS Avg_Customer_Rating,
    ROUND(AVG(Driver_Ratings), 2) AS Avg_Driver_Rating,
    COUNT(Customer_Rating) AS Total_Rated_Bookings
FROM rides
WHERE Customer_Rating IS NOT NULL
GROUP BY Vehicle_Type
ORDER BY Avg_Customer_Rating DESC;


-- ------------------------------------------------------------------------------
-- QUESTION 9: Calculate the total booking value of rides completed successfully
-- Business Context: Fundamental gross merchandise value (GMV) / realized revenue metric for the period.
-- Expected Output: ₹35,080,467 across 63,967 completed rides
-- ------------------------------------------------------------------------------
SELECT 
    SUM(Booking_Value) AS Total_Successful_Booking_Value_INR,
    COUNT(*) AS Total_Completed_Rides,
    ROUND(AVG(Booking_Value), 2) AS Avg_Fare_Per_Ride_INR
FROM rides
WHERE Booking_Status = 'Success';


-- ------------------------------------------------------------------------------
-- QUESTION 10: List all incomplete rides along with the reason
-- Business Context: Tracks operational in-trip friction (breakdowns, route issues, mid-trip rider termination).
-- Expected Output: 3,926 rides
-- ------------------------------------------------------------------------------
SELECT 
    Booking_ID,
    Ride_Date,
    Customer_ID,
    Vehicle_Type,
    Incomplete_Rides,
    Incomplete_Rides_Reason,
    Booking_Value,
    Ride_Distance
FROM rides
WHERE Incomplete_Rides = 'Yes';

-- Incomplete Rides Distribution by Reason:
SELECT 
    Incomplete_Rides_Reason,
    COUNT(*) AS Total_Incomplete_Rides,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rides WHERE Incomplete_Rides = 'Yes'), 2) AS Pct_Share
FROM rides
WHERE Incomplete_Rides = 'Yes'
GROUP BY Incomplete_Rides_Reason
ORDER BY Total_Incomplete_Rides DESC;

