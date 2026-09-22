import pandas as pd
import pandera.pandas as pa



schema =pa.DataFrameSchema(

    {
        "customer_name":pa.Column(str,required=True) ,
        "customer_email":pa.Column(str,nullable=True),
        "customer_id":pa.Column(str,required=True),
        "transaction_id":pa.Column(str,required=True),
        "amount":pa.Column(float,pa.Check.greater_than(0)),
        "currency":pa.Column(str,required=True),
        "timestamp_utc":pa.Column( "datetime64[us, UTC]" ,required=True),
        "status":pa.Column(str,pa.Check.isin(["success","failed","pending","refunded"])),
        "source":pa.Column(str,pa.Check.isin(["stripe","paypal","bank_ach"]))

              }
)


