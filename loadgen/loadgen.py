"""Sends steady traffic to the gateway so dashboards always have data."""
import os
import random
import time

import requests

TARGET = os.getenv("TARGET", "http://gateway:8000/checkout")
RPS = float(os.getenv("RPS", "5"))

print(f"loadgen: {RPS} req/s -> {TARGET}", flush=True)
while True:
    try:
        requests.get(TARGET, timeout=5)
    except requests.RequestException:
        pass
    time.sleep(random.expovariate(RPS))
