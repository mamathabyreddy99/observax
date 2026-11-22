"""payments service: part of the ObservaX demo system."""
import random
import time

from flask import Flask, Response, g, jsonify, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

SERVICE = "payments"
app = Flask(__name__)

REQUESTS = Counter(
    "http_requests_total", "Total HTTP requests",
    ["service", "method", "endpoint", "status"],
)
LATENCY = Histogram(
    "http_request_duration_seconds", "HTTP request latency in seconds",
    ["service", "endpoint"],
    buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5),
)

# Chaos controls: break the service on purpose and watch dashboards react.
chaos = {"latency_ms": 0, "error_rate": 0.0}
SKIP = ("/metrics", "/health", "/chaos")


@app.before_request
def before():
    g.start = time.perf_counter()
    if request.path in SKIP:
        return None
    if chaos["latency_ms"] > 0:
        time.sleep(chaos["latency_ms"] / 1000.0)
    if random.random() < chaos["error_rate"]:
        return jsonify(error="injected failure", service=SERVICE), 500
    return None


@app.after_request
def after(resp):
    if request.path not in SKIP:
        endpoint = request.url_rule.rule if request.url_rule else "unmatched"
        LATENCY.labels(SERVICE, endpoint).observe(time.perf_counter() - g.start)
        REQUESTS.labels(SERVICE, request.method, endpoint, str(resp.status_code)).inc()
    return resp


@app.get("/health")
def health():
    return jsonify(status="ok", service=SERVICE)


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.route("/chaos", methods=["GET", "POST"])
def set_chaos():
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        chaos["latency_ms"] = int(data.get("latency_ms", chaos["latency_ms"]))
        chaos["error_rate"] = float(data.get("error_rate", chaos["error_rate"]))
    return jsonify(service=SERVICE, **chaos)


@app.post("/pay")
def pay():
    time.sleep(random.uniform(0.01, 0.05))  # simulate work
    return jsonify(status="paid", transaction_id=random.randint(100000, 999999))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
