import os
print("Current working directory:", os.getcwd())

import pandas as pd
import pyodbc
import os

# Ensure output directory exists
os.makedirs("outputs", exist_ok=True)

# Connect to SQL Server
conn = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=PRAVEEN\MSSQLSERVER01;"
    "DATABASE=SalesAnalyticsDW;"
    "Trusted_Connection=yes;"
)

query = """
SELECT
    customer_id,
    MAX(order_date) AS last_purchase_date,
    COUNT(DISTINCT sales_key) AS frequency,
    SUM(revenue) AS monetary_value
FROM fact_sales
GROUP BY customer_id;
"""

df_rfm = pd.read_sql(query, conn)
conn.close()

# Convert date
df_rfm['last_purchase_date'] = pd.to_datetime(df_rfm['last_purchase_date'])

# Recency calculation
today = df_rfm['last_purchase_date'].max()
df_rfm['recency'] = (today - df_rfm['last_purchase_date']).dt.days

# RFM Scoring (Quartiles)
df_rfm['R_score'] = pd.qcut(df_rfm['recency'], 4, labels=[4, 3, 2, 1])
df_rfm['F_score'] = pd.qcut(df_rfm['frequency'], 4, labels=[1, 2, 3, 4])
df_rfm['M_score'] = pd.qcut(df_rfm['monetary_value'], 4, labels=[1, 2, 3, 4])

# Composite RFM score
df_rfm['RFM_Score'] = (
    df_rfm['R_score'].astype(str) +
    df_rfm['F_score'].astype(str) +
    df_rfm['M_score'].astype(str)
)

# Business-friendly segmentation
def segment_customer(row):
    if row['R_score'] == 4 and row['F_score'] >= 3 and row['M_score'] >= 3:
        return 'High Value'
    elif row['R_score'] <= 2 and row['F_score'] <= 2:
        return 'At Risk'
    else:
        return 'Regular'

df_rfm['segment'] = df_rfm.apply(segment_customer, axis=1)

# Save output
df_rfm.to_csv("4.outputs/customer_segments.csv", index=False)

print("RFM segmentation completed successfully")
print(df_rfm['segment'].value_counts())
