import os
import pandas as pd

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def transform_custom(*args, **kwargs):
    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your custom logic here

    localFiles = os.listdir('data/')
    localFiles = [f for f in localFiles if '.csv' in f]

    for pos in range(len(localFiles)):

        f = localFiles[pos]
        d_dtypes = {
            'sensor_id': pd.Int64Dtype(),
            'sensor_type':pd.StringDtype(),
            'location':pd.StringDtype(),
            'lat':float,
            'lon':float,
            'timestamp':pd.StringDtype(),
            'value_type':pd.StringDtype(),
            'value': float
        }

        df = pd.read_csv(f'data/{f}', delimiter = ';', dtype=d_dtypes)
        df['timestamp'] = pd.to_datetime(df['timestamp'],
                            format='%Y-%m-%dT%H:%M:%S.%f+00:00')
        df['year'] = df['timestamp'].dt.strftime('%Y').astype('int64')
        df['date'] =  pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d')

        if pos == 0:
            data = df
        else:
            data = pd.concat([data, df])


        data.head(100).to_csv('data_100.csv', index = False)
        print(f'processing file {f} size {df.shape} new size {data.shape}...')

    data.to_parquet('data/sensor-data.parquet') 

    return data