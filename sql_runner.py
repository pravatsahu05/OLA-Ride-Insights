"""
CLI SQL Runner for OLA Ride Insights
Executes and prints all 10 project SQL queries with formatted output.
"""

import sys
import os
import pandas as pd
from src.db_manager import PREDEFINED_SQL_QUERIES, execute_query

def run_all_queries():
    print("=" * 80)
    print("OLA RIDE INSIGHTS - SQL QUERIES EXECUTION REPORT")
    print("=" * 80)

    for name, item in PREDEFINED_SQL_QUERIES.items():
        print(f"\n[{item['id']}] {item['question']}")
        print(f"Description: {item['description']}")
        print(f"Expected: {item['expected_result']}")
        print("-" * 60)
        
        # If the query returns thousands of rows, run summary or preview
        sql_to_run = item.get("count_sql") or item.get("breakdown_sql") or item["sql"]
        if "LIMIT" not in sql_to_run and ("SELECT *" in sql_to_run or "SELECT Booking_ID" in sql_to_run):
            sql_to_run += " LIMIT 5"
        
        df, count, elapsed_ms, err = execute_query(sql_to_run)
        if err:
            print(f"Error: {err}")
        else:
            print(f"Query Result (Executed in {elapsed_ms} ms):")
            print(df.to_string(index=False))
        print("=" * 80)

if __name__ == "__main__":
    run_all_queries()
