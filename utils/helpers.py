import logging
import re
import sys
import yaml

from typing import Tuple
from logging import FileHandler


def sanitize_input(input_string):
    # Remove any characters that are not alphanumeric, underscores, or hyphens
    return re.sub(r"\W+", "", input_string)


def validate_yaml_fields(*args) -> bool:
    return all(arg is not None for arg in args)


def create_log_handler(path: str) -> FileHandler:
    handler = logging.FileHandler(path)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    return handler


def log_summary(output: str, path: str):
    log = logging.getLogger("Run Summary")
    log.setLevel(logging.INFO)

    if not log.handlers:
        handler = create_log_handler(path)
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
