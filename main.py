import configparser
import os
import requests
import sys
import yaml

from utils import helpers


config = configparser.ConfigParser()
config.read("config.ini")


APP_CONFIGS_DIR = config.get("APP_CONFIGS", "MAIN_DIR")


def main():
    target_app = input("Load-test target: ")
    print("Confirming target exists ... \n")

    target_path = verify_target(target_app.lower())
    if not target_path:
        print(f"Target: {target_app} does not exist")
        sys.exit()

    print("Target confirmed, scanning for available tests ... \n")
    target_suite = find_tests(target_path)
    load_test_path = os.path.join(target_path, f"{target_suite}/main.yaml")

    runs = int(input("\n# of required runs: "))
    # default to 1 if less than 1
    (
        load_test(runs=1, path=load_test_path)
        if runs < 1
        else load_test(runs, path=load_test_path)
    )


def verify_target(target: str) -> str:
    target = helpers.sanitize_input(target)
    for item in os.listdir(APP_CONFIGS_DIR):
        if item == target:
            # verify item is a directory
            target_path = os.path.join(APP_CONFIGS_DIR, target)
            return target_path if os.path.isdir(target_path) else ""


def find_tests(path: str) -> str:
    # list existing load test suites
    tests = [
        test_name
        for test_name in os.listdir(path)
        if os.path.isdir(os.path.join(path, test_name))
    ]
    print("===== Existing tests ===== \n")
    for index, test in enumerate(tests):
        print(index, test)

    target_suite = int(input("\nSpecify suite #: "))
    return tests[target_suite]


def run(method, endpoint, status_code):
    response = requests.request(method.upper(), endpoint)

    if response.status_code != int(status_code):
        print("somethings off")
    else:
        print("all good!")


def load_test(runs: int, path: str):
    try:
        with open(path, "r") as file:
            data = yaml.safe_load(file)
    except FileNotFoundError:
        print("Unable to locate setting for load test")
        sys.exit()

    endpoint = data.get("endpoint")
    method = data.get("method")
    expected_status_code = data.get("expected_status_code")

    if helpers.validate_yaml_fields(endpoint, method, expected_status_code):
        while runs != 0:
            run(method, endpoint, status_code=expected_status_code)
            runs -= 1
    else:
        print("field validation failed")


# start the program
main()
