import pandas as pd
import pyodbc
import matplotlib
matplotlib.use("TkAgg")

# SQL Server connection
conn = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=PRAVEEN\MSSQLSERVER01;"
    "DATABASE=SalesAnalyticsDW;"
    "Trusted_Connection=yes;"
)

# Monthly sales dataset
query = """
SELECT
    DATEFROMPARTS(YEAR(order_date), MONTH(order_date), 1) AS sales_month,
    SUM(revenue) AS total_revenue,
    SUM(order_qty) AS total_quantity,
    COUNT(DISTINCT sales_key) AS total_orders
FROM fact_sales
GROUP BY DATEFROMPARTS(YEAR(order_date), MONTH(order_date), 1)
ORDER BY sales_month;
"""

df_sales = pd.read_sql(query, conn)

print(df_sales.head())
conn.close()

import matplotlib.pyplot as plt

df_sales['sales_month'] = pd.to_datetime(df_sales['sales_month'])

plt.figure(figsize=(10, 5))
plt.plot(df_sales['sales_month'], df_sales['total_revenue'])
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.tight_layout()

# Save the plot (VERY IMPORTANT)
plt.savefig("4.outputs/monthly_revenue_trend.png")

plt.show()
df_sales.to_csv("4.outputs/forecast_results.csv", index=False)

