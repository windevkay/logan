import configparser
import os
import requests
import sys
import time

from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from utils import helpers


config = configparser.ConfigParser()
config.read("config.ini")


APP_CONFIGS_DIR = config.get("APP_CONFIGS", "MAIN_DIR")
MAX_WORKERS = config.get("RUN_CONFIGS", "MAX_WORKERS")


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


def run(method: str, endpoint: str) -> int:
    response = requests.request(method.upper(), endpoint)
    return response.status_code


def load_test(runs: int, path: str, log_path: str):
    endpoint, method, expected_status_code = helpers.read_config(path)
    log_path = os.path.join(log_path, "results.log")

    if helpers.validate_yaml_fields(endpoint, method, expected_status_code):
        required_runs = runs
        start_time = time.time()
        status_code_counter = defaultdict(int)
        futures = []

        with ThreadPoolExecutor(max_workers=int(MAX_WORKERS)) as executor:
            pbar = tqdm(total=runs, desc="Running load tests")
            for _ in range(runs):
                future = executor.submit(run, method, endpoint)
                futures.append(future)

            for future in as_completed(futures):
                status_code = future.result()
                status_code_counter[status_code] += 1
                pbar.update(1)

        pbar.close()
        end_time = time.time()
        time_taken = round(end_time - start_time, 2)
        # log summary
        result = f"Runs: {required_runs} | Total time taken: {time_taken} (secs)"
        helpers.log_summary(result, log_path)
        # log status code specifics
        for code, count in status_code_counter.items():
            helpers.log_summary(f"Status Code {code}: {count} times", log_path)
    else:
        print("Field validation failed")


# start the program
main()
