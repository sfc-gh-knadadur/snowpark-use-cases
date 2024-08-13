from tecton import BatchSource, SnowflakeConfig, Entity, batch_feature_view, FeatureService
from datetime import datetime, timedelta
from tecton.types import Float64, String, Timestamp, Field

transactions = BatchSource(
    name='transactions',
    batch_config=SnowflakeConfig(
        url='https://tnb84480.snowflakecomputing.com//',
        database='TRANSACTIONS_DB',
        schema='TRANSACTIONS_SCHEMA',
        warehouse='xs_wh',
        table='TRANSACTIONS',
        timestamp_field = 'TIMESTAMP',
    )
)

user = Entity(name="user", join_keys=["USER_ID"])

from tecton import batch_feature_view


@batch_feature_view(
    sources=[transactions], 
    entities=[user], 
    mode='snowflake_sql',
    online=True,
    offline=True,
    feature_start_time=datetime(2024, 8, 12),
    batch_schedule=timedelta(days=1),
    schema=[Field('USER_ID', String)
        , Field('TIMESTAMP', Timestamp)
        , Field('LAT', Float64)
        , Field('LONG', Float64)
    ]
)
def transaction_location(transactions):
    return f"""
        SELECT
            USER_ID,
            TIMESTAMP,
            LAT,
            LONG
        FROM
            {transactions}
        """

fraud_detection_service = FeatureService(
    name='fraud_detection_service',
    features=[
        transaction_location
    ],
)