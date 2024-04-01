import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here

    data['timestamp'] = pd.to_datetime(data['timestamp'],
                            format='%Y-%m-%dT%H:%M:%S.%f+00:00')
    data['year'] = data['timestamp'].dt.strftime('%Y').astype('int64')
    data['date'] =  pd.to_datetime(data['timestamp']).dt.strftime('%Y-%m-%d')
    data['coordinate'] = data['lat'].astype(str) +','+data['lon'].astype(str) 

    return data