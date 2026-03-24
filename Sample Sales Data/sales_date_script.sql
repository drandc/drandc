-- total revenue by year
select cast("YEAR_ID" as text), SUM("SALES") as revenue
from sales_data_sample
group by "YEAR_ID";

-- monthly trend
SELECT
    cast("YEAR_ID" as text) as year,
    "MONTH_ID" AS month,
    SUM("SALES") AS monthly_revenue,
    COUNT(DISTINCT "ORDERNUMBER") AS order_count
from sales_data_sample
GROUP BY "YEAR_ID", "MONTH_ID"
ORDER BY "YEAR_ID", "MONTH_ID";

-- revenue by country
select "COUNTRY", ROUND(SUM("SALES")) as "SALES"
from sales_data_sample
group by "COUNTRY"
order by "COUNTRY";

-- percentage of total revenue by country
SELECT 
  "COUNTRY",
  ROUND(cast(SUM("SALES") / (SELECT SUM("SALES") FROM sales_data_sample) * 100 as numeric), 2) AS perc_of_total
from sales_data_sample
group by "COUNTRY"
order by "COUNTRY"

-- top 5 products
select "PRODUCTCODE", ROUND(SUM("SALES")) as "SALES"
from sales_data_sample
group by "PRODUCTCODE"
order by SUM("SALES" ) desc
limit 5;

--average order size
select "PRODUCTCODE", ROUND(AVG("QUANTITYORDERED")) as avg_order_size
from sales_data_sample
group by "PRODUCTCODE"
order by AVG("QUANTITYORDERED") desc

-- year-by-year growth per product
select "PRODUCTCODE", 
	ROUND(SUM(case when "YEAR_ID" = 2003 then "SALES"
	else 0 end)) as "SALES_2003", 
	ROUND(SUM(case when "YEAR_ID" = 2004 then "SALES"
	else 0 end)) as "SALES_2004", 
	ROUND(SUM(case when "YEAR_ID" = 2005 then "SALES"
	else 0 end)) as "SALES_2005" 
from sales_data_sample
group by "PRODUCTCODE"
order by "PRODUCTCODE"

-- year-by-year growth by product line
select "PRODUCTLINE", 
	ROUND(SUM(case when "YEAR_ID" = 2003 then "SALES"
	else 0 end)) as "SALES_2003", 
	ROUND(SUM(case when "YEAR_ID" = 2004 then "SALES"
	else 0 end)) as "SALES_2004", 
	ROUND(SUM(case when "YEAR_ID" = 2005 then "SALES"
	else 0 end)) as "SALES_2005" 
from sales_data_sample
group by "PRODUCTLINE"
order by "PRODUCTLINE" 

-- order count and average revenue per customer
select "CUSTOMERNAME", COUNT(*) as num_of_orders, ROUND(AVG("SALES")) as avg_order_value
from sales_data_sample
group by "CUSTOMERNAME" 
order by "CUSTOMERNAME"


