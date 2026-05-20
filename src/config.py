import os
import yaml

root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

class MainConfig:
    @staticmethod
    def get_root():
        return root
    @staticmethod
    def get_config_data() -> dict:
        with open(os.path.join(root, 'configs','main.yml'), 'r') as f:
            return yaml.safe_load(f)
