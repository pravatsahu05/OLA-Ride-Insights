"""
OLA Ride Insights - Data Preprocessing & Pipeline Module
Handles data cleaning, normalization, feature engineering, and database storage.
"""

import os
import sqlite3
import pandas as pd
import numpy as np

def assign_time_bucket(hour):
    if 6 <= hour < 12:
        return 'Morning (06:00-11:59)'
    elif 12 <= hour < 17:
        return 'Afternoon (12:00-16:59)'
    elif 17 <= hour < 22:
        return 'Evening (17:00-21:59)'
    else:
        return 'Night (22:00-05:59)'

def preprocess_ola_data(input_csv="ola_rides.csv", output_csv="data/ola_rides_cleaned.csv", db_path="data/ola_rides.db"):
    print("[1/5] Loading raw ride data...")
    if os.path.exists(input_csv):
        df = pd.read_csv(input_csv)
    elif os.path.exists("OLA_DataSet.xlsx"):
        df = pd.read_excel("OLA_DataSet.xlsx", sheet_name="July")
    else:
        raise FileNotFoundError("Raw dataset not found.")

    print(f"Loaded {len(df):,} records.")

    print("[2/5] Standardizing datetime features...")
    # Standardize Date
    df['Date'] = pd.to_datetime(df['Date'])
    df['Ride_Date'] = df['Date'].dt.date.astype(str)
    
    # Standardize Time and extract hour
    df['Time_Str'] = df['Time'].astype(str).str.strip()
    # Extract hour safely
    df['Ride_Hour'] = df['Time_Str'].apply(lambda x: int(x.split(':')[0]) if ':' in x else 0)
    df['Day_Name'] = df['Date'].dt.day_name()
    df['Day_Of_Week'] = df['Date'].dt.dayofweek
    df['Is_Weekend'] = df['Day_Of_Week'].apply(lambda x: 1 if x in [5, 6] else 0)
    df['Time_Of_Day'] = df['Ride_Hour'].apply(assign_time_bucket)

    print("[3/5] Cleaning and standardizing categorical & numerical fields...")
    # String strip
    str_cols = ['Booking_ID', 'Booking_Status', 'Customer_ID', 'Vehicle_Type', 
                'Pickup_Location', 'Drop_Location', 'Payment_Method', 
                'Canceled_Rides_by_Customer', 'Canceled_Rides_by_Driver', 
                'Incomplete_Rides', 'Incomplete_Rides_Reason']
    for c in str_cols:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip()
            df.loc[df[c].isin(['nan', 'None', '']), c] = np.nan

    # Numerical types
    num_cols = ['Booking_Value', 'Ride_Distance', 'V_TAT', 'C_TAT', 'Driver_Ratings', 'Customer_Rating']
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')

    print("[4/5] Exporting cleaned CSV...")
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False)
    # Also save to root for easy fallback
    df.to_csv("ola_rides_cleaned.csv", index=False)

    print("[5/5] Storing in SQLite database...")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    for target_db in [db_path, "ola_rides.db"]:
        conn = sqlite3.connect(target_db)
        df.to_sql('rides', conn, if_exists='replace', index=False)
        cursor = conn.cursor()
        # Create indexes for high query performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_booking_status ON rides(Booking_Status);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_vehicle_type ON rides(Vehicle_Type);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_payment_method ON rides(Payment_Method);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_customer_id ON rides(Customer_ID);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_ride_date ON rides(Ride_Date);")
        conn.commit()
        conn.close()

    print(f"Preprocessing completed successfully! Output saved to:\n  - {output_csv}\n  - {db_path} and root ola_rides.db")
    return df

if __name__ == "__main__":
    preprocess_ola_data()
