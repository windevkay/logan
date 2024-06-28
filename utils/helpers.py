import logging
import re
import sys
import yaml

from typing import Tuple


def sanitize_input(input_string):
    # Remove any characters that are not alphanumeric, underscores, or hyphens
    return re.sub(r"\W+", "", input_string)


def validate_yaml_fields(*args) -> bool:
    return all(arg is not None for arg in args)


def load_test_run_log(output: str, log_file_path: str):
    log = logging.getLogger("load test")
    log.setLevel(logging.INFO)

    handler = logging.FileHandler(log_file_path)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    log.addHandler(handler)
    log.info(output)


def read_config(config_path: str) -> Tuple[str, str, int]:
    try:
        with open(config_path, "r") as file:
            data = yaml.safe_load(file)
    except FileNotFoundError:
        print("Unable to locate configs for load test")
        sys.exit(1)

    config = data.get("main")
    return (
        config.get("endpoint"),
        config.get("method"),
        config.get("expected_status_code"),
    )
