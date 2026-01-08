USE SalesAnalyticsDW;
GO

-- Monthly Sales Analytics Table
IF OBJECT_ID('fact_sales_forecast') IS NOT NULL
    DROP TABLE fact_sales_forecast;

CREATE TABLE fact_sales_forecast (
    sales_month DATE,
    total_revenue DECIMAL(18,2),
    total_quantity INT,
    total_orders INT
);

-- Customer Segmentation Table
IF OBJECT_ID('dim_customer_segment') IS NOT NULL
    DROP TABLE dim_customer_segment;

CREATE TABLE dim_customer_segment (
    customer_id INT,
    recency INT,
    frequency INT,
    monetary_value DECIMAL(18,2),
    RFM_Score VARCHAR(10),
    segment VARCHAR(20)
);
