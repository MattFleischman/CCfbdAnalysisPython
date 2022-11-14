from __future__ import print_function
import time
import cfbd
import pandas as pd
from cfbd.rest import ApiException
from pprint import pprint


def init_config(api_key):
    # Configure API key authorization: ApiKeyAuth
    auth_configuration = cfbd.Configuration()
    auth_configuration.api_key['Authorization'] = api_key
    auth_configuration.api_key_prefix['Authorization'] = 'Bearer'
    return auth_configuration


def get_cfbd_data(api_class, api_method, auth_configuration, filter_configs):
    api_instance = api_class(cfbd.ApiClient(auth_configuration))

    try:
        # Coaching records and history
        api_response = getattr(api_instance, api_method)(**filter_configs)

    except ApiException as e:
        raise Exception
    converted_dict = {}
    for k in api_response[0].to_dict():
        converted_dict[k] = []

    for row in api_response:
        for k, v in row.to_dict().items():
            converted_dict[k].append(v)
    print(f"converted_dict: {converted_dict}")

    return pd.DataFrame(converted_dict)