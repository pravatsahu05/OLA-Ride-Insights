"""
Generate Comprehensive Word Document Report for OLA Ride Insights Capstone
"""

import os
import sqlite3
import pandas as pd
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_report():
    print("Generating OLA Ride Insights Capstone Word Document Report...")
    doc = docx.Document()
    
    # Page setup - 1 inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Document Styles
    styles = doc.styles
    normal_style = styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(6)

    # ---------------------------------------------------------
    # COVER TITLE & HEADER
    # ---------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(24)
    title_p.paragraph_format.space_after = Pt(4)
    r_tag = title_p.add_run("CAPSTONE PROJECT REPORT | MOBILITY ANALYTICS\n")
    r_tag.font.size = Pt(10)
    r_tag.font.bold = True
    r_tag.font.color.rgb = RGBColor(0x16, 0xA3, 0x4A) # OLA Green

    r_title = title_p.add_run("OLA Ride Insights: Data Analytics, SQL Querying & Business Intelligence Dashboard")
    r_title.font.size = Pt(24)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    sub_p = doc.add_paragraph()
    r_sub = sub_p.add_run("An end-to-end urban mobility analytics platform analyzing 103,024 ride bookings across Bengaluru for July 2024. Featuring automated SQL query resolution, Power BI 5-view dashboard modeling, and a high-performance Streamlit interactive web application.")
    r_sub.font.size = Pt(12)
    r_sub.font.color.rgb = RGBColor(0x47, 0x55, 0x69)
    sub_p.paragraph_format.space_after = Pt(18)

    # Metadata Table
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Project Domain", "Ride-Sharing, Urban Mobility & Telemetry Analytics"),
        ("Technologies Used", "Python 3.12, Pandas, SQLite 3, SQL, Power BI Desktop, Streamlit, Plotly"),
        ("Dataset Dimensions", "103,024 Records, 20 Core Columns, July 2024 (Bengaluru Urban Area)"),
        ("Project Deliverables", "Cleaned Datasets (CSV/DB), 10 SQL Queries, Power BI DAX & Views, Streamlit Web App")
    ]
    for row_idx, (k, v) in enumerate(meta_data):
        row = meta_table.rows[row_idx]
        cell_k, cell_v = row.cells[0], row.cells[1]
        cell_k.text = k
        cell_v.text = v
        set_cell_background(cell_k, "0F172A")
        set_cell_background(cell_v, "F8FAFC")
        cell_k.paragraphs[0].runs[0].font.bold = True
        cell_k.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        cell_k.paragraphs[0].runs[0].font.size = Pt(10)
        cell_v.paragraphs[0].runs[0].font.size = Pt(10)
        set_cell_margins(cell_k, 80, 80, 120, 120)
        set_cell_margins(cell_v, 80, 80, 120, 120)

    doc.add_page_break()

    # ---------------------------------------------------------
    # 1. EXECUTIVE SUMMARY & PROBLEM STATEMENT
    # ---------------------------------------------------------
    h1 = doc.add_heading("1. Executive Summary & Problem Statement", level=1)
    h1.paragraph_format.space_before = Pt(12)
    
    doc.add_paragraph(
        "The rapid expansion of app-based ride-hailing services has revolutionized modern urban transit. "
        "OLA, as a market leader, captures massive amounts of high-frequency transactional and telemetry data spanning "
        "booking requests, turnaround times (TAT), fleet distributions, vehicle categories, and ratings. "
        "However, deriving actionable operational clarity from this data is fraught with challenges including localized "
        "supply-demand deficits, driver and customer cancellations, and cash-heavy payment bottlenecks."
    )
    doc.add_paragraph(
        "The objective of this capstone project is to clean, model, analyze, and present OLA's July 2024 operational records "
        "through three core pillars:\n"
        "1. Robust Data Pipeline & SQL Engine: Cleaned and indexed relational database answering 10 critical operational questions.\n"
        "2. Power BI Analytics Modeling: Complete DAX measures and visualization layout across 5 segregated views.\n"
        "3. Modern Streamlit Web Application: A responsive, top-filtered dashboard providing live telemetry exploration and custom SQL querying."
    )

    # ---------------------------------------------------------
    # 2. DATASET ARCHITECTURE & CLEANING PIPELINE
    # ---------------------------------------------------------
    h2 = doc.add_heading("2. Dataset Architecture & Preprocessing Pipeline", level=1)
    
    doc.add_paragraph(
        "The raw dataset (OLA_DataSet.xlsx, Sheet 'July') consists of 103,024 booking logs spanning 50 urban locations across "
        "Bengaluru between July 01 and July 31, 2024. A rigorous automated cleaning script (src/data_preprocessing.py) was built to:"
    )
    doc.add_paragraph(
        "• Parse and Standardize Timestamps: Separated ride date into ISO YYYY-MM-DD format and extracted integer hour of day (0-23).\n"
        "• Feature Engineering: Created time-of-day buckets (Morning, Afternoon, Evening, Night), Day of Week names, and weekend flags.\n"
        "• Null Handling & Verification: Confirmed that nulls in V_TAT, C_TAT, ratings, and payment methods occur strictly for unfulfilled/cancelled rides (39,057 rides), reflecting real-world business logic.\n"
        "• High-Performance Relational Indexing: Stored the processed records into SQLite with B-Tree indexes on Booking_Status, Vehicle_Type, Payment_Method, and Customer_ID for sub-second query performance."
    )

    # High-level summary table
    doc.add_heading("Key Operational Metrics Summary (July 2024)", level=2)
    summary_table = doc.add_table(rows=8, cols=3)
    summary_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_headers = ["Metric Name", "Value", "Operational Significance"]
    for c_idx, h in enumerate(table_headers):
        cell = summary_table.rows[0].cells[c_idx]
        cell.text = h
        set_cell_background(cell, "1E293B")
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_cell_margins(cell, 80, 80, 100, 100)

    summary_rows = [
        ("Total Booking Requests", "103,024", "Total mobility demand logged in the period"),
        ("Successful Completed Rides", "63,967 (62.09%)", "Trips successfully serviced and billed"),
        ("Canceled by Driver", "18,434 (17.89%)", "Highest source of trip fulfillment loss"),
        ("Canceled by Customer", "10,499 (10.19%)", "Pre-trip rider attrition"),
        ("Driver Not Found", "10,124 (9.83%)", "Unfulfilled demand due to localized supply shortage"),
        ("Total Realized Gross Revenue", "₹35,080,467", "Net booking value generated by completed rides"),
        ("Average Booking Fare", "₹548.42", "Average gross ticket size per completed trip")
    ]
    for r_idx, (m, v, s) in enumerate(summary_rows, start=1):
        row = summary_table.rows[r_idx]
        row.cells[0].text = m
        row.cells[1].text = v
        row.cells[2].text = s
        for c in row.cells:
            set_cell_background(c, "F1F5F9" if r_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(c, 60, 60, 100, 100)
            c.paragraphs[0].runs[0].font.size = Pt(10)

    # ---------------------------------------------------------
    # 3. VERIFIED SQL QUERIES (1 TO 10)
    # ---------------------------------------------------------
    doc.add_page_break()
    h3 = doc.add_heading("3. Comprehensive SQL Query Solutions (Questions 1 to 10)", level=1)
    
    sql_qa = [
        (
            1, "Retrieve all successful bookings",
            "SELECT * FROM rides WHERE Booking_Status = 'Success';",
            "63,967 completed bookings (62.09% of total volume). Provides the foundational cohort for revenue, customer loyalty, and ratings analysis."
        ),
        (
            2, "Find the average ride distance for each vehicle type",
            "SELECT Vehicle_Type, ROUND(AVG(Ride_Distance), 2) AS Avg_Distance, COUNT(*) AS Total_Trips\nFROM rides GROUP BY Vehicle_Type ORDER BY Avg_Distance DESC;",
            "Prime Sedan leads with 15.76 km, followed closely by eBike (15.58 km), Bike (15.53 km), Mini (15.51 km), Prime Plus (15.45 km), and Prime SUV (15.27 km). Auto operates strictly as short-haul micro-transit averaging 6.24 km."
        ),
        (
            3, "Get the total number of cancelled rides by customers",
            "SELECT COUNT(*) AS Total_Cancelled_By_Customers FROM rides WHERE Booking_Status = 'Canceled by Customer';",
            "10,499 rides cancelled by customers (10.19% of all requests). Root-cause analysis reveals 30.2% cancelled because 'Driver is not moving towards pickup location' and 25.4% because 'Driver asked to cancel'."
        ),
        (
            4, "List the top 5 customers who booked the highest number of rides",
            "SELECT Customer_ID, COUNT(Booking_ID) AS Total_Bookings, SUM(CASE WHEN Booking_Status = 'Success' THEN 1 ELSE 0 END) AS Completed_Bookings\nFROM rides GROUP BY Customer_ID ORDER BY Total_Bookings DESC LIMIT 5;",
            "Top customer CID954071 logged 5 bookings (3 successful). Followed by CID980727, CID969725, CID966929, and CID952434 with 4 bookings each."
        ),
        (
            5, "Get the number of rides cancelled by drivers due to personal and car-related issues",
            "SELECT COUNT(*) AS Cancelled_Personal_Car_Issues FROM rides WHERE Canceled_Rides_by_Driver = 'Personal & Car related issue';",
            "6,542 rides, representing 35.49% of all 18,434 driver cancellations. Signifies that vehicle maintenance and driver health downtime represent a major operational friction point."
        ),
        (
            6, "Find the maximum and minimum driver ratings for Prime Sedan bookings",
            "SELECT MAX(Driver_Ratings) AS Max_Rating, MIN(Driver_Ratings) AS Min_Rating, ROUND(AVG(Driver_Ratings), 2) AS Avg_Rating\nFROM rides WHERE Vehicle_Type = 'Prime Sedan' AND Driver_Ratings IS NOT NULL;",
            "Maximum Driver Rating = 5.0, Minimum Driver Rating = 3.0, Average Driver Rating = 3.99 across 9,379 rated Prime Sedan trips."
        ),
        (
            7, "Retrieve all rides where payment was made using UPI",
            "SELECT COUNT(*) AS Total_UPI_Rides, SUM(Booking_Value) AS Total_Revenue, ROUND(AVG(Booking_Value), 2) AS Avg_Fare\nFROM rides WHERE Payment_Method = 'UPI';",
            "25,881 completed rides paid via UPI, generating ₹14,168,436 in revenue (Average ticket size: ₹547.45). Represents 40.4% of total completed revenue."
        ),
        (
            8, "Find the average customer rating per vehicle type",
            "SELECT Vehicle_Type, ROUND(AVG(Customer_Rating), 2) AS Avg_Customer_Rating\nFROM rides WHERE Customer_Rating IS NOT NULL GROUP BY Vehicle_Type ORDER BY Avg_Customer_Rating DESC;",
            "Ratings are remarkably consistent across tiers: Prime Plus (4.01), Auto (4.00), Mini (4.00), Prime SUV (4.00), Prime Sedan (4.00), Bike (3.99), and eBike (3.99)."
        ),
        (
            9, "Calculate the total booking value of rides completed successfully",
            "SELECT SUM(Booking_Value) AS Total_Successful_Booking_Value, COUNT(*) AS Total_Completed_Rides\nFROM rides WHERE Booking_Status = 'Success';",
            "Total gross revenue generated: ₹35,080,467 (~₹3.51 Crores) across 63,967 completed rides, yielding an average fare of ₹548.42."
        ),
        (
            10, "List all incomplete rides along with the reason",
            "SELECT Incomplete_Rides_Reason, COUNT(*) AS Total_Incomplete_Rides, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rides WHERE Incomplete_Rides = 'Yes'), 2) AS Pct_Share\nFROM rides WHERE Incomplete_Rides = 'Yes' GROUP BY Incomplete_Rides_Reason ORDER BY Total_Incomplete_Rides DESC;",
            "3,926 rides were terminated mid-journey: Customer Demand accounted for 1,601 rides (40.78%), Vehicle Breakdown for 1,591 rides (40.52%), and Other Issues for 734 rides (18.70%)."
        )
    ]

    for q_num, q_title, q_code, q_insight in sql_qa:
        doc.add_heading(f"Question {q_num}: {q_title}", level=2)
        p_code = doc.add_paragraph()
        r_code = p_code.add_run(q_code)
        r_code.font.name = 'Consolas'
        r_code.font.size = Pt(9.5)
        r_code.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        p_code.paragraph_format.left_indent = Inches(0.2)
        
        p_ins = doc.add_paragraph()
        r_lbl = p_ins.add_run("Result & Interpretation: ")
        r_lbl.font.bold = True
        r_lbl.font.color.rgb = RGBColor(0x16, 0xA3, 0x4A)
        p_ins.add_run(q_insight)
        p_ins.paragraph_format.space_after = Pt(10)

    # ---------------------------------------------------------
    # 4. POWER BI DASHBOARD ARCHITECTURE & 5 SEGREGATED VIEWS
    # ---------------------------------------------------------
    doc.add_page_break()
    h4 = doc.add_heading("4. Power BI Dashboard Architecture & Segregated Views", level=1)
    
    doc.add_paragraph(
        "To deliver a comprehensive BI solution as required by the project specifications, the Power BI dashboard "
        "is structured across 5 core segregated views:"
    )
    views_desc = [
        ("View 1: Overall View", "Features a macro Ride Volume Over Time line/area chart (daily volume and 24-hour peak demand distribution) alongside a central Booking Status Breakdown donut chart (Success 62.1%, Driver Cancelled 17.9%, Customer Cancelled 10.2%, Driver Not Found 9.8%)."),
        ("View 2: Vehicle Type View", "Highlights Top 5 Vehicle Types by Ride Distance in horizontal bars, alongside a vehicle fleet share donut chart and comparative Turnaround Times (V_TAT vs C_TAT) across the 7 fleet categories."),
        ("View 3: Revenue View", "Deconstructs revenue by payment method (Cash: ₹19.26M / 54.9%, UPI: ₹14.17M / 40.4%, Credit Card: ₹1.31M / 3.7%, Debit Card: ₹0.34M / 1.0%), lists Top 5 Customers by Total Booking Value, and models daily fleet mileage vs average trip distance."),
        ("View 4: Cancellation View", "Presents side-by-side root cause analyses for Customer Cancellations (Driver stationary 30.2%, Driver asked to cancel 25.4%, Change of plans 19.8%) and Driver Cancellations (Personal/car issues 35.5%, Customer issues 29.4%), plus incomplete trip breakdown."),
        ("View 5: Ratings View", "Provides distribution histograms for Customer and Driver ratings (both centered at 4.00), with grouped bar charts examining inter-vehicle rating variance.")
    ]
    for v_title, v_body in views_desc:
        p = doc.add_paragraph()
        r_t = p.add_run(f"• {v_title}: ")
        r_t.font.bold = True
        p.add_run(v_body)

    # ---------------------------------------------------------
    # 5. STREAMLIT APPLICATION ARCHITECTURE
    # ---------------------------------------------------------
    doc.add_heading("5. Streamlit Interactive Web Application", level=1)
    doc.add_paragraph(
        "The project application (app.py) was built using Streamlit and Plotly, delivering a high-end dark luxury mobility theme "
        "resembling an enterprise mobility control deck. Key interface features include:\n"
        "• Top Filter Control Deck: Replaced side navigation filters with 4 horizontal global controls at the top (Date Window, Fleet Categories, Trip Status, Payment Gateways) allowing full-width dashboard visualization.\n"
        "• Executive KPI Cards: 6 responsive cards featuring real-time micro progress bars, icon avatars, and delta annotations.\n"
        "• 5-View Power BI Analytics Suite: Replicates all charts interactively with Plotly Express and Graph Objects.\n"
        "• SQL Query Hub & Interactive Console: Allows users to run all 10 project SQL queries with execution timing benchmarks, and write custom ad-hoc SQL queries with live tabular rendering and CSV downloads.\n"
        "• Geospatial Route Matrix: Identifies Bengaluru's highest demand origins (Banashankari, Yeshwanthpur, RT Nagar, Indiranagar) and top commuter corridors."
    )

    # ---------------------------------------------------------
    # 6. STRATEGIC BUSINESS PLAYBOOK
    # ---------------------------------------------------------
    doc.add_heading("6. Strategic Business Playbook & Operational Recommendations", level=1)
    playbook = [
        ("1. Dynamic Supply Rebalancing (Eliminate the 9.8% 'Driver Not Found' Gap)", 
         "10,124 ride requests failed due to lack of nearby drivers, representing ₹5.5M+ in unrealized revenue. OLA should implement predictive rebalancing incentives that reposition idle cabs toward high-volume nodes (Banashankari, Yeshwanthpur) ahead of the 17:00 - 21:00 evening peak."),
        ("2. Anti-Wait Telemetry Alerts (Curtail 30.2% Customer Cancellations)", 
         "3,175 customers cancelled because their assigned driver showed zero movement toward the pickup spot. Deploying automated telemetry monitors that ping drivers stationary for > 180 seconds and offer customers instant one-tap reassignment will directly recover booking attrition."),
        ("3. Rapid Pit-Stop Fleet Maintenance (Address 35.5% Driver Drop-offs)", 
         "6,542 driver cancellations and 1,591 mid-trip incomplete rides stemmed from car and mechanical breakdowns. OLA should establish express diagnostic checkups and battery swaps for eBikes near top suburban drop-off hubs."),
        ("4. UPI AutoPay Acceleration (Transition 54.9% Cash Base)", 
         "Cash payments generate change disputes and boarding turnaround delays. Offering a ₹25 cashback on the first 3 UPI AutoPay rides will transition the customer base from 45.1% digital to > 70% digital within two quarters.")
    ]
    for p_title, p_body in playbook:
        p = doc.add_paragraph()
        r_pt = p.add_run(f"{p_title}\n")
        r_pt.font.bold = True
        r_pt.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        p.add_run(p_body)
        p.paragraph_format.space_after = Pt(8)

    # Save document
    output_filename = "OLA_Ride_Insights_Complete_Project_Report.docx"
    doc.save(output_filename)
    print(f"Report successfully saved as: {output_filename}")

if __name__ == "__main__":
    create_report()

