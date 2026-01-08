USE SalesAnalyticsDW;
GO

-- Monthly Sales Aggregation (Forecast-Ready)
SELECT
    DATEFROMPARTS(YEAR(fs.order_date), MONTH(fs.order_date), 1) AS sales_month,
    SUM(fs.sales_amount) AS total_sales,
    SUM(fs.quantity) AS total_quantity,
    COUNT(DISTINCT fs.order_id) AS total_orders
FROM fact_sales fs
GROUP BY
    DATEFROMPARTS(YEAR(fs.order_date), MONTH(fs.order_date), 1)
ORDER BY sales_month;
