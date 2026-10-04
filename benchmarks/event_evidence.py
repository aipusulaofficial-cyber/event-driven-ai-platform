"""Concurrent HTTP event-publication evidence for CI acceptance."""

import importlib
import json
import statistics
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
app = importlib.import_module("service").app


def run(requests=200, workers=16):
    if requests < 1 or workers < 1:
        raise ValueError("requests and workers must be positive")
    latencies = []
    failures = 0

    def one(index):
        started = time.perf_counter()
        with TestClient(app) as client:
            response = client.post(
                "/v1/events",
                json={
                    "key": f"event-{index}",
                    "payload": {"topic": "distinguished-evidence", "data": {"index": index}},
                },
            )
        latency = (time.perf_counter() - started) * 1000
        body = response.json() if response.status_code == 200 else {}
        ok = response.status_code == 200 and body.get("status") == "published"
        return latency, ok

    wall_started = time.perf_counter()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(one, index) for index in range(requests)]
        for future in as_completed(futures):
            latency, ok = future.result()
            latencies.append(latency)
            failures += int(not ok)
    wall_s = time.perf_counter() - wall_started
    ordered = sorted(latencies)

    def pct(q):
        index = min(len(ordered) - 1, max(0, int((len(ordered) - 1) * q)))
        return ordered[index]

    return {
        "requests": requests,
        "workers": workers,
        "failures": failures,
        "error_rate": failures / requests,
        "throughput_rps": round(requests / wall_s, 2),
        "latency_ms": {
            "p50": round(statistics.median(ordered), 3),
            "p95": round(pct(0.95), 3),
            "p99": round(pct(0.99), 3),
        },
        "workload": "FastAPI TestClient -> /v1/events -> Event.create -> broker.publish",
        "measurement": "repeatable CI HTTP event-publication acceptance benchmark; not a production hardware claim",
    }


if __name__ == "__main__":
    report = run()
    destination = Path("artifacts/event-domain-evidence.json")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
