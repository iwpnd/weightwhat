import pandas as pd
import json
import requests
import time
import concurrent.futures
from loguru import logger
import datetime


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        logger.info(
            "{:s} function took {:.3f} ms".format(f.__name__, (time2 - time1) * 1000.0)
        )

        return ret

    return wrap


df = pd.read_csv("weight.csv", usecols=["Date", "Weight (kg)"], parse_dates=True)
df.columns = ["created_at", "weight"]
df = df.sort_values(by="created_at", ascending=True).reset_index(drop=True)


def post_single(weight: float, created_at: datetime = None) -> int:
    data = {"weight": weight, "created_at": created_at}
    # logger.debug(f"received {data}")
    response = requests.post("http://localhost:8002/api/weight", json=data)
    # logger.debug(f"status: {response.status_code}")
    return f"status_code: {response.status_code}"


@timing
def post_many():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        args = ((weight, date) for weight, date in zip(df.weight, df.created_at))
        results = executor.map(lambda p: post_single(*p), args)
        logger.debug(f"processed: {len([result for result in results])}")


if __name__ == "__main__":
    post_many()
