import logging
import os
import time

import yaml

LOG_DIR = os.path.join("logs")
LOG_FORMAT = "%(levelname)s %(name)s %(asctime)s - %(message)s"

if not os.path.isdir(LOG_DIR):
    os.mkdir(LOG_DIR)

log_filename = os.path.join(LOG_DIR, "crawling.log")


def get_logger(logger_name):
    logging.basicConfig(filename=log_filename, level=logging.INFO, format=LOG_FORMAT)
    logger = logging.getLogger(logger_name)

    return logger


def load_yaml(field, path="config.yaml"):
    with open(path, "r") as f:
        config = yaml.load(f, yaml.SafeLoader)
    return config[field]


def load_stopwords():
    path = load_yaml("paths")["stopwords"]
    with open(path, "r") as f:
        stopwords = f.read().split("\n")
    return stopwords


def timing(method):
    def timed(*args, **kwargs):
        start = time.time()
        result = method(*args, **kwargs)
        end = time.time()

        execution_time = end - start
        if execution_time < 0.001:
            print(
                f"{method.__name__} took {round(execution_time * 1000, 3)} milliseconds"
            )
        else:
            print(f"{method.__name__} took {round(execution_time, 3)} seconds")

        return result

    return timed
