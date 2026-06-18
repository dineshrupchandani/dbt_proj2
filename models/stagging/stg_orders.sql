with orders as
(
    select 
    101 as order_id,
    'C1' as customer_id,
    -- 2. Categorical Dimensions
    'success' as order_status_code,
    -- 3. Time Dimensions (Must be fully qualified timestamps/dates)
    date('20260101','YYYYMMDD') as order_date
    
    union all

    select 
    102 as order_id,
    'C1' as customer_id,
    -- 2. Categorical Dimensions
    'success' as order_status_code,
    -- 3. Time Dimensions (Must be fully qualified timestamps/dates)
    date('20260101','YYYYMMDD') as order_date
    
    union all

select 
    103 as order_id,
    'C1' as customer_id,
    -- 2. Categorical Dimensions
    'fail' as order_status_code,
    -- 3. Time Dimensions (Must be fully qualified timestamps/dates)
    date('20260101','YYYYMMDD') as order_date
    
    union all
select 
    104 as order_id,
    'C1' as customer_id,
    -- 2. Categorical Dimensions
    'success' as order_status_code,
    -- 3. Time Dimensions (Must be fully qualified timestamps/dates)
    date('20260101','YYYYMMDD') as order_date
    
    union all
select 
    105 as order_id,
    'C1' as customer_id,
    -- 2. Categorical Dimensions
    'success' as order_status_code,
    -- 3. Time Dimensions (Must be fully qualified timestamps/dates)
    date('20260101','YYYYMMDD') as order_date
    
    union all
select 
    106 as order_id,
    'C1' as customer_id,
    -- 2. Categorical Dimensions
    'success' as order_status_code,
    -- 3. Time Dimensions (Must be fully qualified timestamps/dates)
    date('20260201','YYYYMMDD') as order_date
    
    union all
select 
    107 as order_id,
    'C1' as customer_id,
    -- 2. Categorical Dimensions
    'success' as order_status_code,
    -- 3. Time Dimensions (Must be fully qualified timestamps/dates)
    date('20260201','YYYYMMDD') as order_date
    
    union all
select 
    108 as order_id,
    'C1' as customer_id,
    -- 2. Categorical Dimensions
    'success' as order_status_code,
    -- 3. Time Dimensions (Must be fully qualified timestamps/dates)
    date('20260201','YYYYMMDD') as order_date
    
    union all
select 
    109 as order_id,
    'C1' as customer_id,
    -- 2. Categorical Dimensions
    'success' as order_status_code,
    -- 3. Time Dimensions (Must be fully qualified timestamps/dates)
    date('20260201','YYYYMMDD') as order_date
    
    union all
select 
    110 as order_id,
    'C1' as customer_id,
    -- 2. Categorical Dimensions
    'success' as order_status_code,
    -- 3. Time Dimensions (Must be fully qualified timestamps/dates)
    date('20260301','YYYYMMDD') as order_date
    
    union all
select 
    111 as order_id,
    'C1' as customer_id,
    -- 2. Categorical Dimensions
    'success' as order_status_code,
    -- 3. Time Dimensions (Must be fully qualified timestamps/dates)
    date('20260301','YYYYMMDD') as order_date
    
    union all
select 
    112 as order_id,
    'C1' as customer_id,
    -- 2. Categorical Dimensions
    'fail' as order_status_code,
    -- 3. Time Dimensions (Must be fully qualified timestamps/dates)
    date('20260301','YYYYMMDD') as order_date
    


)
select * from orders