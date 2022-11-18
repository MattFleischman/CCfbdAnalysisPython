import datetime
import sys
import stat_ingestion.cfbd_api_ingestion as cfbd_api_ingestion
import stat_transformations.cfbd_data_transformations as data_transformations
import utilities.utility_functions as utilities


#TODO: look into adding queue + threading to speed up data ingestion time

if __name__ == '__main__':
    run_configs = ['data_transform']
    # pull configs
    yaml_configs = utilities.read_configurations('stat_ingestion/cfbd_api_configurations.yaml')
    if 'date_extract' in run_configs:
        for api_type in yaml_configs['ingestion_configs']['api_type']:
            print(f"api_type: {api_type}")
            api_configs = utilities.clean_api_configs(yaml_configs['ingestion_configs']['api_type'][api_type])

            # pull data
            api_key = open('C:/Users/mattf/cfbd_analytics/other/api_key.txt', 'r').read()
            api_auth_config = cfbd_api_ingestion.init_config(
                api_key=api_key)
            api_class = api_configs['api_class']['name']
            for method in api_configs['api_class']['api_methods']:

                filter_configs = api_configs['api_class']['api_methods'][method]['filter_config']
                print(method)

                api_response = cfbd_api_ingestion.get_cfbd_data(api_class=getattr(sys.modules['cfbd'], api_class),
                                                                api_method=method,
                                                                auth_configuration=api_auth_config,
                                                                filter_configs=filter_configs)
                api_response.to_csv(f"C:/Users/mattf/cfbd_analytics/file_stage/{api_type}_{method}_data_extract_{datetime.datetime.now().strftime('%Y%m%d%H')}.txt", sep='|')
    if 'data_transform' in run_configs:
        performance_adjusted_team_recruiting = data_transformations.transform_performing_player_recruiting()
