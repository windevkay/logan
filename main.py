import configparser
import os
import requests
import sys
import time

from utils import helpers


config = configparser.ConfigParser()
config.read("config.ini")


APP_CONFIGS_DIR = config.get("APP_CONFIGS", "MAIN_DIR")


def main():
    target_app = input("Load-test target (app): ")
    print("Confirming target exists ... \n")

    target_path = verify_target(target_app.lower())
    if not target_path:
        print(f"Target: {target_app} does not exist")
        sys.exit(1)

    print("Target (app) confirmed, scanning for available tests ... \n")
    target_suite = find_tests(target_path)
    load_test_path = os.path.join(target_path, f"{target_suite}/test_config.yaml")
    log_path = os.path.join(target_path, target_suite)

    runs = int(input("\n# of required runs: "))
    # default to 1 if less than 1
    load_test(1 if runs < 1 else runs, load_test_path, log_path)


def verify_target(target: str) -> str | None:
    target = helpers.sanitize_input(target)
    for item in os.listdir(APP_CONFIGS_DIR):
        if item == target:
            # verify item is a directory
            target_path = os.path.join(APP_CONFIGS_DIR, target)
            return target_path if os.path.isdir(target_path) else None
    return None


def find_tests(path: str) -> str:
    # list existing load test suites
    tests = [
        test_name
        for test_name in os.listdir(path)
        if os.path.isdir(os.path.join(path, test_name))
    ]
    if len(tests) > 0:
        print("===== Existing tests ===== \n")
        for index, test in enumerate(tests):
            print(index, test)

        target_suite = int(input("\nSpecify suite #: "))
        return tests[target_suite]
    else:
        print("No existing test suites within specified path")
        sys.exit(1)


def run(method, endpoint, status_code):
    response = requests.request(method.upper(), endpoint)

    if response.status_code != status_code:
        print("Unexpected status code", response.status_code)


def load_test(runs: int, path: str, log_path: str):
    endpoint, method, expected_status_code = helpers.read_config(path)

    if helpers.validate_yaml_fields(endpoint, method, expected_status_code):
        required_runs = runs
        start_time = time.time()

        while runs != 0:
            run(method, endpoint, expected_status_code)
            runs -= 1

        end_time = time.time()
        time_taken = round(end_time - start_time, 2)

        result = f"Runs: {required_runs} | Total time taken: {time_taken} (secs)"
        helpers.load_test_run_log(result, os.path.join(log_path, "results.log"))
    else:
        print("Field validation failed")


# start the program
main()
