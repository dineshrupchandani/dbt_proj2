with payments as
(
    select 1 as id, 100 as payment_amount, 'success' as payment_status, 101 as order_id
    union all
    select 2 as id, 100 as payment_amount, 'success' as payment_status, 102 as order_id
    union all
    select 3 as id, 100 as payment_amount, 'fail' as payment_status, 103 as order_id
    union all
    select 4 as id, 100 as payment_amount, 'success' as payment_status, 104 as order_id
    union all
    select 5 as id, 100 as payment_amount, 'fail' as payment_status, 105 as order_id
    union all
    select 6 as id, 100 as payment_amount, 'success' as payment_status, 106 as order_id

)
select * from payments