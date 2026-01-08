USE SalesAnalyticsDW;
GO

-- Customer-Level Metrics for RFM Analysis
SELECT
    c.customer_id,
    MAX(fs.order_date) AS last_purchase_date,
    COUNT(DISTINCT fs.order_id) AS frequency,
    SUM(fs.sales_amount) AS monetary_value
FROM fact_sales fs
JOIN dim_customer c
    ON fs.customer_id = c.customer_id
GROUP BY
    c.customer_id;
