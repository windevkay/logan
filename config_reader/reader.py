import sys
import yaml


class Config_Reader:
    def __init__(self, config_path: str):
        self.config_path = config_path

    def read_config(self):
        try:
            with open(self.config_path, "r") as file:
                data = yaml.safe_load(file)
        except FileNotFoundError:
            print("Unable to locate configs for load test")
            sys.exit()

        config = data.get("main")
        return (
            config.get("endpoint"),
            config.get("method"),
            config.get("expected_status_code"),
        )
