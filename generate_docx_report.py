"""
Generate Comprehensive Word Document Report for OLA Ride Insights Capstone
Includes clickable hyperlinks, zero empty spaces, continuous flow, and full end-to-end deliverables.
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

def add_hyperlink(paragraph, url, text, color="0066CC", underline=True, bold=True):
    """Inserts a genuine clickable hyperlink into a Word paragraph."""
    part = paragraph.part
    r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)
    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)

    new_run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')

    if color:
        c = OxmlElement('w:color')
        c.set(qn('w:val'), color)
        rPr.append(c)

    if underline:
        u = OxmlElement('w:u')
        u.set(qn('w:val'), 'single')
        rPr.append(u)

    if bold:
        b = OxmlElement('w:b')
        rPr.append(b)

    new_run.append(rPr)
    new_run.text = text
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_report():
    print("Generating Complete OLA Ride Insights Word Document Report (No Empty Spaces & Clickable Links)...")
    doc = docx.Document()
    
    # 0.8 inch margins to maximize usable area and prevent awkward empty gaps
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    styles = doc.styles
    normal_style = styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)

    # ---------------------------------------------------------
    # COVER / HEADER
    # ---------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(2)
    r_tag = title_p.add_run("CAPSTONE PROJECT REPORT | URBAN MOBILITY ANALYTICS\n")
    r_tag.font.size = Pt(10)
    r_tag.font.bold = True
    r_tag.font.color.rgb = RGBColor(0x16, 0xA3, 0x4A) # OLA Green

    r_title = title_p.add_run("OLA Ride Insights: End-to-End Mobility Analytics & Intelligence")
    r_title.font.size = Pt(20)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    sub_p = doc.add_paragraph()
    r_sub = sub_p.add_run("Comprehensive Operational Analysis of 103,024 Ride Bookings across Bengaluru (July 2024), featuring automated SQL telemetry queries, Power BI DAX modeling, and a modernized Streamlit interactive web application.")
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = RGBColor(0x4B, 0x55, 0x63)
    sub_p.paragraph_format.space_after = Pt(8)

    # ---------------------------------------------------------
    # CLICKABLE LINKS BANNER (AT THE VERY BEGINNING)
    # ---------------------------------------------------------
    link_table = doc.add_table(rows=2, cols=2)
    link_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Header row
    cell_h1, cell_h2 = link_table.rows[0].cells[0], link_table.rows[0].cells[1]
    cell_h1.text = "Deployment Channel"
    cell_h2.text = "Direct Clickable Access URL"
    set_cell_background(cell_h1, "0F172A")
    set_cell_background(cell_h2, "0F172A")
    cell_h1.paragraphs[0].runs[0].font.bold = True
    cell_h1.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    cell_h1.paragraphs[0].runs[0].font.size = Pt(10)
    cell_h2.paragraphs[0].runs[0].font.bold = True
    cell_h2.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    cell_h2.paragraphs[0].runs[0].font.size = Pt(10)
    set_cell_margins(cell_h1, 60, 60, 100, 100)
    set_cell_margins(cell_h2, 60, 60, 100, 100)

    # Row 1: Web App
    row1 = link_table.rows[1]
    row1.cells[0].text = "🌐 Live Interactive Web App"
    set_cell_background(row1.cells[0], "F1F5F9")
    set_cell_background(row1.cells[1], "F1F5F9")
    row1.cells[0].paragraphs[0].runs[0].font.bold = True
    row1.cells[0].paragraphs[0].runs[0].font.size = Pt(10)
    p_link1 = row1.cells[1].paragraphs[0]
    p_link1.text = ""
    add_hyperlink(p_link1, "https://ola-ride-insights-pravatsahu05.streamlit.app/", "https://ola-ride-insights-pravatsahu05.streamlit.app/", color="0284C7", underline=True, bold=True)
    set_cell_margins(row1.cells[0], 60, 60, 100, 100)
    set_cell_margins(row1.cells[1], 60, 60, 100, 100)

    # Add GitHub Repo row
    row2 = link_table.add_row()
    row2.cells[0].text = "💻 GitHub Source Code Repository"
    set_cell_background(row2.cells[0], "FFFFFF")
    set_cell_background(row2.cells[1], "FFFFFF")
    row2.cells[0].paragraphs[0].runs[0].font.bold = True
    row2.cells[0].paragraphs[0].runs[0].font.size = Pt(10)
    p_link2 = row2.cells[1].paragraphs[0]
    p_link2.text = ""
    add_hyperlink(p_link2, "https://github.com/pravatsahu05/OLA-Ride-Insights", "https://github.com/pravatsahu05/OLA-Ride-Insights", color="0284C7", underline=True, bold=True)
    set_cell_margins(row2.cells[0], 60, 60, 100, 100)
    set_cell_margins(row2.cells[1], 60, 60, 100, 100)

    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(4)
    p_spacer.paragraph_format.space_after = Pt(6)

    # ---------------------------------------------------------
    # PROJECT SPECIFICATIONS TABLE
    # ---------------------------------------------------------
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Project Domain", "Ride-Sharing, Telemetry Analytics & Urban Micro-Transit Optimization"),
        ("Technology Stack", "Python 3.12, Pandas, SQLite 3, SQL, Power BI Desktop, Streamlit, Plotly"),
        ("Dataset Dimensions", "103,024 Records, 20 Core Columns, July 01 to July 31, 2024 (Bengaluru Urban Area)"),
        ("Core Deliverables", "Cleaned Datasets (CSV/DB), 10 SQL Queries, Power BI DAX & Views, Streamlit Web App, Executive Report")
    ]
    for row_idx, (k, v) in enumerate(meta_data):
        row = meta_table.rows[row_idx]
        cell_k, cell_v = row.cells[0], row.cells[1]
        cell_k.text = k
        cell_v.text = v
        set_cell_background(cell_k, "1E293B")
        set_cell_background(cell_v, "F8FAFC" if row_idx % 2 == 0 else "FFFFFF")
        cell_k.paragraphs[0].runs[0].font.bold = True
        cell_k.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        cell_k.paragraphs[0].runs[0].font.size = Pt(9.5)
        cell_v.paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_margins(cell_k, 50, 50, 100, 100)
        set_cell_margins(cell_v, 50, 50, 100, 100)

    # ---------------------------------------------------------
    # 1. EXECUTIVE SUMMARY & PROBLEM STATEMENT
    # ---------------------------------------------------------
    h1 = doc.add_heading("1. Executive Summary & Problem Statement", level=1)
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(4)
    h1.paragraph_format.keep_with_next = True
    
    doc.add_paragraph(
        "Modern urban ride-hailing networks operate in hyper-dynamic, high-density environments. OLA captures millions of telemetry "
        "and booking data points encompassing passenger demand, vehicle dispatch, turnaround times (TAT), driver cancellations, "
        "and customer ratings. Without systematic data modeling and business intelligence, operational friction—such as driver "
        "supply deficits, unfulfilled ride requests, and localized vehicle breakdowns—directly impairs profitability and customer retention."
    )
    doc.add_paragraph(
        "This project models and analyzes OLA's operational footprint across Bengaluru for the month of July 2024 (103,024 records). "
        "The project systematically delivers: (1) an automated data preprocessing & relational SQL engine solving 10 key operational questions, "
        "(2) a complete Power BI architecture covering 5 distinct views and DAX measures, (3) an interactive modern Streamlit web application "
        "providing live telemetry filtering and real-time SQL execution, and (4) actionable business recommendations."
    )

    # ---------------------------------------------------------
    # 2. DATASET ARCHITECTURE & OPERATIONAL SUMMARY
    # ---------------------------------------------------------
    h2 = doc.add_heading("2. Dataset Architecture & Operational Performance", level=1)
    h2.paragraph_format.space_before = Pt(10)
    h2.paragraph_format.space_after = Pt(4)
    h2.paragraph_format.keep_with_next = True

    doc.add_paragraph(
        "The dataset encompasses 103,024 ride requests logged between July 01, 2024 and July 31, 2024 across 50 primary pickup and drop nodes in Bengaluru. "
        "The preprocessing pipeline normalized timestamps into ISO dates, extracted 24-hour time indices, categorized rush periods, "
        "and established B-Tree indexing on primary operational dimensions."
    )

    # Summary KPI Table
    summary_table = doc.add_table(rows=8, cols=3)
    summary_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_headers = ["Key Performance Metric", "Value / Volume", "Operational Significance"]
    for c_idx, h in enumerate(table_headers):
        cell = summary_table.rows[0].cells[c_idx]
        cell.text = h
        set_cell_background(cell, "0F172A")
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        cell.paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_margins(cell, 60, 60, 100, 100)

    summary_rows = [
        ("Total Ride Booking Requests", "103,024", "Total logged passenger demand across Bengaluru in July 2024"),
        ("Successful Completed Rides", "63,967 (62.09%)", "Trips successfully fulfilled, boarded, and billed"),
        ("Cancellations by Drivers", "18,434 (17.89%)", "Primary leakage point; highest proportion of lost fulfillment"),
        ("Cancellations by Customers", "10,499 (10.19%)", "Pre-trip rider attrition caused by driver delays or re-routing"),
        ("Driver Not Found (Unfulfilled)", "10,124 (9.83%)", "Unmet demand attributable to localized fleet supply deficits"),
        ("Total Realized Gross Revenue", "₹35,080,467", "Cumulative gross booking fare collected from completed trips"),
        ("Average Booking Fare", "₹548.42", "Average gross revenue yield per completed trip")
    ]
    for r_idx, (m, v, s) in enumerate(summary_rows, start=1):
        row = summary_table.rows[r_idx]
        row.cells[0].text = m
        row.cells[1].text = v
        row.cells[2].text = s
        for c_i, c in enumerate(row.cells):
            set_cell_background(c, "F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(c, 50, 50, 100, 100)
            c.paragraphs[0].runs[0].font.size = Pt(9.5)
            if c_i == 1:
                c.paragraphs[0].runs[0].font.bold = True

    # ---------------------------------------------------------
    # 3. VERIFIED SQL QUERIES (1 TO 10)
    # ---------------------------------------------------------
    h3 = doc.add_heading("3. SQL Query Solutions & Business Interpretations (Questions 1 to 10)", level=1)
    h3.paragraph_format.space_before = Pt(12)
    h3.paragraph_format.space_after = Pt(4)
    h3.paragraph_format.keep_with_next = True

    sql_qa = [
        (
            1, "Retrieve all successful bookings",
            "SELECT * FROM rides WHERE Booking_Status = 'Success';",
            "63,967 completed bookings (62.09% completion rate). Represents the revenue-generating baseline for customer loyalty, ticket sizes, and rating evaluations."
        ),
        (
            2, "Find the average ride distance for each vehicle type",
            "SELECT Vehicle_Type, ROUND(AVG(Ride_Distance), 2) AS Avg_Distance, COUNT(*) AS Total_Trips\nFROM rides GROUP BY Vehicle_Type ORDER BY Avg_Distance DESC;",
            "Prime Sedan recorded the highest average distance (15.76 km), closely followed by eBike (15.58 km), Bike (15.53 km), Mini (15.51 km), Prime Plus (15.45 km), and Prime SUV (15.27 km). Auto operates strictly as short-haul micro-transit (6.24 km)."
        ),
        (
            3, "Get the total number of cancelled rides by customers",
            "SELECT COUNT(*) AS Total_Cancelled_By_Customers FROM rides WHERE Booking_Status = 'Canceled by Customer';",
            "10,499 rides were cancelled by customers (10.19% of total requests). Analysis reveals that 30.2% were cancelled because the 'Driver is not moving towards pickup location' and 25.4% because the 'Driver asked customer to cancel'."
        ),
        (
            4, "List the top 5 customers who booked the highest number of rides",
            "SELECT Customer_ID, COUNT(Booking_ID) AS Total_Bookings, SUM(CASE WHEN Booking_Status = 'Success' THEN 1 ELSE 0 END) AS Completed_Bookings\nFROM rides GROUP BY Customer_ID ORDER BY Total_Bookings DESC LIMIT 5;",
            "Top user CID954071 placed 5 bookings (3 completed). CID980727, CID969725, CID966929, and CID952434 followed with 4 bookings each."
        ),
        (
            5, "Get the number of rides cancelled by drivers due to personal and car-related issues",
            "SELECT COUNT(*) AS Cancelled_Personal_Car_Issues FROM rides WHERE Canceled_Rides_by_Driver = 'Personal & Car related issue';",
            "6,542 rides were cancelled due to personal & car issues, representing 35.49% of all 18,434 driver cancellations. Highlights vehicle reliability and driver downtime as primary operational vulnerabilities."
        ),
        (
            6, "Find the maximum and minimum driver ratings for Prime Sedan bookings",
            "SELECT MAX(Driver_Ratings) AS Max_Rating, MIN(Driver_Ratings) AS Min_Rating, ROUND(AVG(Driver_Ratings), 2) AS Avg_Rating\nFROM rides WHERE Vehicle_Type = 'Prime Sedan' AND Driver_Ratings IS NOT NULL;",
            "Maximum Rating = 5.0, Minimum Rating = 3.0, Average Rating = 3.99 across 9,379 rated Prime Sedan trips, demonstrating stable service quality."
        ),
        (
            7, "Retrieve all rides where payment was made using UPI",
            "SELECT COUNT(*) AS Total_UPI_Rides, SUM(Booking_Value) AS Total_Revenue, ROUND(AVG(Booking_Value), 2) AS Avg_Fare\nFROM rides WHERE Payment_Method = 'UPI';",
            "25,881 completed rides were transacted via UPI, accounting for ₹14,168,436 (40.39% of total revenue) with an average ticket size of ₹547.45."
        ),
        (
            8, "Find the average customer rating per vehicle type",
            "SELECT Vehicle_Type, ROUND(AVG(Customer_Rating), 2) AS Avg_Customer_Rating\nFROM rides WHERE Customer_Rating IS NOT NULL GROUP BY Vehicle_Type ORDER BY Avg_Customer_Rating DESC;",
            "Customer satisfaction is exceptionally uniform: Prime Plus (4.01), Auto (4.00), Mini (4.00), Prime SUV (4.00), Prime Sedan (4.00), Bike (3.99), and eBike (3.99)."
        ),
        (
            9, "Calculate the total booking value of rides completed successfully",
            "SELECT SUM(Booking_Value) AS Total_Successful_Booking_Value, COUNT(*) AS Total_Completed_Rides\nFROM rides WHERE Booking_Status = 'Success';",
            "Total gross realized revenue was ₹35,080,467 (~₹3.51 Crores) across 63,967 completed rides, resulting in an average fare of ₹548.42."
        ),
        (
            10, "List all incomplete rides along with the reason",
            "SELECT Incomplete_Rides_Reason, COUNT(*) AS Total_Incomplete_Rides, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rides WHERE Incomplete_Rides = 'Yes'), 2) AS Pct_Share\nFROM rides WHERE Incomplete_Rides = 'Yes' GROUP BY Incomplete_Rides_Reason ORDER BY Total_Incomplete_Rides DESC;",
            "3,926 rides were aborted mid-journey. Primary triggers: Customer Demand (1,601 rides / 40.78%), Vehicle Breakdown (1,591 rides / 40.52%), and Other Issues (734 rides / 18.70%)."
        )
    ]

    for q_num, q_title, q_code, q_insight in sql_qa:
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(6)
        p_q.paragraph_format.space_after = Pt(2)
        p_q.paragraph_format.keep_with_next = True
        r_q = p_q.add_run(f"SQL Question {q_num}: {q_title}")
        r_q.font.bold = True
        r_q.font.size = Pt(11)
        r_q.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

        p_code = doc.add_paragraph()
        p_code.paragraph_format.space_before = Pt(2)
        p_code.paragraph_format.space_after = Pt(2)
        p_code.paragraph_format.left_indent = Inches(0.15)
        p_code.paragraph_format.keep_with_next = True
        r_code = p_code.add_run(q_code)
        r_code.font.name = 'Consolas'
        r_code.font.size = Pt(9)
        r_code.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

        p_ins = doc.add_paragraph()
        p_ins.paragraph_format.space_before = Pt(2)
        p_ins.paragraph_format.space_after = Pt(6)
        r_tag = p_ins.add_run("Result & Business Insight: ")
        r_tag.font.bold = True
        r_tag.font.color.rgb = RGBColor(0x16, 0xA3, 0x4A)
        r_text = p_ins.add_run(q_insight)
        r_text.font.size = Pt(10)

    # ---------------------------------------------------------
    # 4. POWER BI DASHBOARD ARCHITECTURE & 5 SEGREGATED VIEWS
    # ---------------------------------------------------------
    h4 = doc.add_heading("4. Power BI Architecture & 5 Segregated Views", level=1)
    h4.paragraph_format.space_before = Pt(12)
    h4.paragraph_format.space_after = Pt(4)
    h4.paragraph_format.keep_with_next = True

    doc.add_paragraph(
        "In accordance with project requirements, the business intelligence layer is organized into 5 dedicated views, "
        "powered by modular DAX measures (Total Bookings, Booking Value, Success Rate, Cancellation Rates, Driver/Customer Averages):"
    )

    views_data = [
        ("View 1: Overall View", "Macro telemetry featuring Ride Volume Over Time (24h diurnal curve with 18:00 peak) and central Booking Status Breakdown (Success 62.1%, Driver Cancelled 17.9%, Customer Cancelled 10.2%, Driver Not Found 9.8%)."),
        ("View 2: Vehicle Type View", "Fleet segmentation analyzing Top 5 Vehicle Types by Ride Distance, vehicle market share, and comparative Turnaround Times (V_TAT vs C_TAT)."),
        ("View 3: Revenue View", "Breakdown by Payment Method (Cash: ₹19.26M / 54.9%, UPI: ₹14.17M / 40.4%, Credit Card: ₹1.31M / 3.7%, Debit Card: ₹0.34M / 1.0%), Top 5 Customers by Booking Value, and Daily Revenue trends."),
        ("View 4: Cancellation View", "Granular root-cause analysis isolating Customer Cancellations (Driver stationary 30.2%, Driver asked to cancel 25.4%) vs Driver Cancellations (Personal/car issues 35.5%, Customer issues 29.4%), alongside mid-journey aborted trips."),
        ("View 5: Ratings View", "Distribution histograms and cross-vehicle satisfaction matrices for Driver Ratings (mean 3.99) and Customer Ratings (mean 4.00).")
    ]
    for v_title, v_desc in views_data:
        p_v = doc.add_paragraph()
        p_v.paragraph_format.space_before = Pt(2)
        p_v.paragraph_format.space_after = Pt(3)
        r_vt = p_v.add_run(f"• {v_title}: ")
        r_vt.font.bold = True
        r_vt.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        p_v.add_run(v_desc)

    # ---------------------------------------------------------
    # 5. STREAMLIT APPLICATION ARCHITECTURE
    # ---------------------------------------------------------
    h5 = doc.add_heading("5. Modern Streamlit Interactive Web Application", level=1)
    h5.paragraph_format.space_before = Pt(12)
    h5.paragraph_format.space_after = Pt(4)
    h5.paragraph_format.keep_with_next = True

    doc.add_paragraph(
        "The project application (app.py) is hosted live at https://ola-ride-insights-pravatsahu05.streamlit.app/. "
        "It features an obsidian dark-matte aesthetic (#0D0F12) with neon electric-volt accents (#D4FF00), engineered for executive decision-makers:"
    )
    doc.add_paragraph(
        "• Top Horizontal Filter Deck: Replaced sidebar controls with full-width global filters (Date Range, Vehicle Type, Booking Status, Payment Method) situated directly under the executive header, unlocking maximum horizontal real estate.\n"
        "• Mandatory Callout Cards: Every visualization card incorporates a verified '💡 Insight' badge highlighting data trends and a '🎯 Business Action' badge detailing operational recommendations.\n"
        "• Real-Time SQL Studio: Provides a built-in interactive console where analysts can execute all 10 pre-configured queries or write custom SQL against the indexed SQLite database with instant tabular outputs and CSV export.\n"
        "• Zero-Dead-Click Guarantee: Removed all unclickable pseudo-badges and dead controls to provide a frictionless interactive user experience."
    )

    # ---------------------------------------------------------
    # 6. STRATEGIC RECOMMENDATIONS & OPERATIONAL PLAYBOOK
    # ---------------------------------------------------------
    h6 = doc.add_heading("6. Strategic Business Playbook & Operational Roadmap", level=1)
    h6.paragraph_format.space_before = Pt(12)
    h6.paragraph_format.space_after = Pt(4)
    h6.paragraph_format.keep_with_next = True

    recommendations = [
        ("1. Dynamic Fleet Rebalancing (Curtail 9.8% 'Driver Not Found' Deficit)",
         "10,124 unfulfilled rides resulted from localized driver shortages, forfeiting ₹5.5M+ in potential revenue. Deploy predictive driver relocation incentives to position vehicles near top demand origin hubs (Banashankari, Yeshwanthpur) prior to peak evening hours (17:00–21:00)."),
        ("2. Automated Stationary Driver Telemetry (Mitigate 30.2% Customer Cancellations)",
         "3,175 customers cancelled because their assigned driver remained stationary. Implement an automated telemetry ping if a vehicle shows no movement after 180 seconds, accompanied by a 1-tap customer reassignment feature."),
        ("3. Express Vehicle Diagnostics & Battery Hubs (Reduce 35.5% Driver Cancellations)",
         "6,542 driver cancellations and 1,591 incomplete trips stemmed from vehicle issues. OLA should launch quick-service maintenance checkups and rapid battery swap stations near high-density suburban transit corridors."),
        ("4. UPI AutoPay Transition (Migrate the 54.9% Cash Heavy Base)",
         "Cash accounts for ₹19.26M in collections, introducing cash-handling overhead and change disputes. A ₹25 fare incentive on the first 3 AutoPay rides will drive digital payment penetration from 45.1% to > 70%.")
    ]

    for r_num, (r_title, r_desc) in enumerate(recommendations, start=1):
        p_r = doc.add_paragraph()
        p_r.paragraph_format.space_before = Pt(3)
        p_r.paragraph_format.space_after = Pt(2)
        p_r.paragraph_format.keep_with_next = True
        r_rt = p_r.add_run(r_title)
        r_rt.font.bold = True
        r_rt.font.size = Pt(10.5)
        r_rt.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

        p_rd = doc.add_paragraph()
        p_rd.paragraph_format.space_before = Pt(1)
        p_rd.paragraph_format.space_after = Pt(5)
        p_rd.add_run(r_desc)

    # Save document
    output_filename = "OLA_Ride_Insights_Complete_Project_Report.docx"
    doc.save(output_filename)
    print(f"Report successfully saved as: {output_filename}")

if __name__ == "__main__":
    create_report()
