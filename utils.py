import json
import configparser
from collections import defaultdict


class ConfigConverter(object):
    def __init__(self):
        self.config = self.get_config()

    @staticmethod
    def get_config():
        config = configparser.ConfigParser()
        config.read("config.ini")
        return config

    def convert_config_to_dict(self):
        config_dict = defaultdict(dict)
        for section in self.config.sections():
            for k, v in self.config.items(section):
                config_dict[section][k] = v

        return config_dict

    def convert_config_to_json(self, output_json):
        config_dict = self.convert_config_to_dict()
        json.dump(config_dict, fp=open(output_json, 'w'), indent=2)


if __name__ == "__main__":
    u = ConfigConverter()
    u.convert_config_to_json("./config.json")
