-- models/marts/fct_orders.sql

{{ config(
    materialized='table',
    unique_key='order_id'
) }}

with orders as (
    select * from {{ ref('stg_orders') }}
),

payments as (
    select * from {{ ref('stg_payments') }}
),

order_payments as (
    select
        order_id,
        sum(payment_amount) as total_amount_paid
    from payments
    group by 1
)

select
    -- 1. Primary & Foreign Entities (Essential for Semantic Joins)
    orders.order_id,
    orders.customer_id,

    -- 2. Categorical Dimensions
    orders.order_status_code as status_code,
    
    -- 3. Time Dimensions (Must be fully qualified timestamps/dates)
    orders.order_date as ordered_at,

    -- 4. Raw Measures (The columns your aggregations will build upon)
    coalesce(order_payments.total_amount_paid, 0) as order_amount

from orders
left join order_payments 
    on orders.order_id = order_payments.order_id