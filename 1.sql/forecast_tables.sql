USE SalesAnalyticsDW;
GO

-- Product-Level Monthly Trends
SELECT
    p.product_id,
    DATEFROMPARTS(YEAR(fs.order_date), MONTH(fs.order_date), 1) AS sales_month,
    SUM(fs.sales_amount) AS product_sales,
    SUM(fs.quantity) AS product_quantity
FROM fact_sales fs
JOIN dim_product p
    ON fs.product_id = p.product_id
GROUP BY
    p.product_id,
    DATEFROMPARTS(YEAR(fs.order_date), MONTH(fs.order_date), 1)
ORDER BY
    p.product_id,
    sales_month;
