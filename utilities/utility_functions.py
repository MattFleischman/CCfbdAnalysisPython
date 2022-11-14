import yaml


def read_configurations(config_path):
    yaml_file = open(config_path, 'r').read()
    yaml_configs = yaml.load(yaml_file, Loader=yaml.Loader)
    return yaml_configs


def clean_api_configs(config):
    for method in config['api_class']['api_methods']:
        method_filter = config['api_class']['api_methods'][method]['filter_config']

        method_filter_configs = {} if method_filter is None else {k: v for k, v in method_filter.items() if v is not None}
        config['api_class']['api_methods'][method]['filter_config'] = method_filter_configs
    return config
