from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from pandas import DataFrame
import pyarrow as pa
import pyarrow.parquet as pq
# from os import path
import os
import pandas as pd

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "CREDS/data-engineering-akl-f0e843d40edd.json"
bucket_name = 'data-engineering-akl-training'
object_key = 'sensor-project'


# bucket_name = 'data-engineering-akl-training'
# project_id = 'sensor-project'
# table_name = "data-partitioned"
root_path = f'{bucket_name}/{object_key}'

df = pd.read_csv('data.csv')

@data_exporter
def export_data_to_google_cloud_storage(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to a Google Cloud Storage bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#googlecloudstorage
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = 'data-engineering-akl-training'
    object_key = 'sensor-project.parquet'

    GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).export(
        df,
        bucket_name,
        object_key,
    )