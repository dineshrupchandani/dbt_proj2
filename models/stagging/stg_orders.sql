with orders as
(
    select 
    101 as order_id,
    'C1' as customer_id,

    -- 2. Categorical Dimensions
    'success' as order_status_code,
    
    -- 3. Time Dimensions (Must be fully qualified timestamps/dates)
    '20260101' as order_date

)
select * from orders