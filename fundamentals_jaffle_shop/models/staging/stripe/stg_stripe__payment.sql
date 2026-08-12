with 

source as (

    select * from {{ source('stripe', 'payment') }}

),

renamed as (

    select
        id as payment_id,
        orderid as order_id,
        paymentmethod,
        -- amount is stored in cents, convert it to dollars
        amount/100 as payment_amount,
        created as created_at,
        status as payment_status,
        _batched_at

    from source

)

select * from renamed