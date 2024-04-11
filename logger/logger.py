import logging


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
