import pandas as pd
import pyodbc

# Connect to SQL Server
conn = pyodbc.connect(
    r"DRIVER={SQL Server};"
    r"SERVER=PRAVEEN\MSSQLSERVER01;"
    r"DATABASE=SalesAnalyticsDW;"
    r"Trusted_Connection=yes;"
)

cursor = conn.cursor()

# Load CSVs
df_sales = pd.read_csv("4.outputs/forecast_results.csv")
df_customers = pd.read_csv("4.outputs/customer_segments.csv")

# Insert sales analytics
for _, row in df_sales.iterrows(): 
    cursor.execute("""
        INSERT INTO fact_sales_forecast
        VALUES (?, ?, ?, ?)
    """,
    row['sales_month'],
    row['total_revenue'],
    row['total_quantity'],
    row['total_orders']
    )

# Insert customer segments
for _, row in df_customers.iterrows():
    cursor.execute("""
        INSERT INTO dim_customer_segment
        VALUES (?, ?, ?, ?, ?, ?)
    """,
    row['customer_id'],
    row['recency'],
    row['frequency'],
    row['monetary_value'],
    row['RFM_Score'],
    row['segment']
    )

conn.commit()
conn.close()

print("Analytics tables populated successfully")
