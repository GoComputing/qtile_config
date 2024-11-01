import yaml
import os


def load_yaml(path):

    with open(path, 'r') as f:
        data = yaml.safe_load(f)

    return data


def load_configs(configs_dir):

    filenames = [
        'general',
        'keybindings',
    ]

    configs = {
        name: load_yaml(os.path.join(configs_dir, f'{name}.yml'))
        for name in filenames
    }

    return configs
