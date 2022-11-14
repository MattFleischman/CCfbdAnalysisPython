import yaml
import sys
import stat_ingestion.cfbd_api_ingestion as cfbd_api_ingestion
import utilities.utility_functions as utilities

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # pull configs
    yaml_configs = utilities.read_configurations('stat_ingestion/cfbd_api_configurations.yaml')
    recruiting_configs = utilities.clean_api_configs(
        yaml_configs['ingestion_configs']['api_type']['recruiting'])
    #print(recruiting_configs)

    # pull data
    api_auth_config = cfbd_api_ingestion.init_config(
        api_key='')
    api_class = recruiting_configs['api_class']['name']
    for method in recruiting_configs['api_class']['api_methods']:

        api_method = method
        filter_configs = recruiting_configs['api_class']['api_methods'][method]['filter_config']
        print(api_class, api_method, api_auth_config, filter_configs)

        api_response = cfbd_api_ingestion.get_cfbd_data(api_class=getattr(sys.modules['cfbd'], api_class),
                                                        api_method=api_method,
                                                        auth_configuration=api_auth_config,
                                                        filter_configs=filter_configs)
        print(f"Method: {api_method} - \nResponse: \n{api_response}")
