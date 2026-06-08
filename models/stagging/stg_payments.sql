with payments as
(
    select 1 as id, 100 as payment_amount, 'success' as payment_status, 101 as order_id
)
select * from payments