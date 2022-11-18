import yaml
import datetime
import stat_ingestion.cfbd_api_ingestion as cfbd_api_ingestion
import sys


def read_configurations(config_path):
    yaml_file = open(config_path, 'r').read()
    yaml_configs = yaml.load(yaml_file, Loader=yaml.Loader)
    return yaml_configs


def clean_api_configs(config):
    for method in config['api_class']['api_methods']:
        method_filter = config['api_class']['api_methods'][method]['filter_config']
        method_filter_configs = {} if method_filter is None else {k: v for k, v in method_filter.items() if (v is not None or k in ['year'])}
        try:
            if method_filter_configs['year'] is None:
                    current_year = int(datetime.datetime.now().strftime('%Y'))
                    method_filter_configs['year'] = list(range(2013, current_year)) + [current_year]
                    print(method_filter_configs['year'])
            '''else 'week' in method_filter_configs & method_filter_configs['week'] is None:
                method_filter_configs['week'] = range(0, 14) + [14]
            else 'team' in method_filter_configs & method_filter_configs['team'] is None:
                api_auth_config = cfbd_api_ingestion.init_config(
                    api_key='XbfBgZjizImMF81QPIho2e68olGYRSRCmZJzFU6DbwPPJj+BoGM1CflXMZjTQ7TS')
                team_df = cfbd_api_ingestion.get_cfbd_data(api_class=getattr(sys.modules['cfbd'], 'TeamsApi'),
                                                                api_method='get_fbs_teams',
                                                                auth_configuration=api_auth_config,
                                                                filter_configs={'year': int(datetime.datetime.now().strftime('%Y'))})
                teams_list = team_df['school'].values.to_list()
                method_filter_configs['teams'] = teams_list
            '''
        except KeyError:
            print("list key does not exist in config")

        config['api_class']['api_methods'][method]['filter_config'] = method_filter_configs
    return config
