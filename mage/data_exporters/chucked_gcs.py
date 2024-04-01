import pyarrow as pa
import pyarrow.parquet as pq
import os
import datetime
import pandas as pd

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "CREDS/data-engineering-akl-f0e843d40edd.json"

bucket_name = 'sensor-project'
project_id = "data-engineering-akl"

table_name = 'data-partitioned.parquet'

root_path = f'{bucket_name}/{table_name}'

@data_exporter
def export_data(data, *args, **kwargs):
    # data['maxdate']='2023-08-29T01:01:01'
    # data['maxdate']=pd.to_datetime(data['maxdate'], format='%Y-%m-%dT%H:%M:%S').dt.date
    # # data['month'] = pd.to_datetime(data['date'], format='%Y-%m')
    # data = data[data['date']>data['maxdate']]
    # data.drop(columns='maxdate',inplace=True)
    # print(data['date'].unique())
    # data['lpep_dropoff_datetime'] = data['lpep_dropoff_datetime'].dt.date

    table = pa.Table.from_pandas(data)

    gcs = pa.fs.GcsFileSystem()

    pq.write_to_dataset(
        table,
        root_path=root_path,
        partition_cols = ['date'],
        filesystem=gcs
    )