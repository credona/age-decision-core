import time
import statistics
import requests

URL = "http://localhost:8000/estimate"
IMAGE_PATH = "test-face.jpg"

ITERATIONS = 20
TIMEOUT = 5


def run():
    durations = []
    success = 0

    for i in range(ITERATIONS):
        with open(IMAGE_PATH, "rb") as f:
            start = time.perf_counter()

            response = requests.post(
                URL,
                files={"file": ("test-face.jpg", f, "image/jpeg")},
                timeout=TIMEOUT,
            )

            duration = time.perf_counter() - start
            durations.append(duration)

        if response.status_code == 200:
            success += 1
        else:
            print(f"[ERROR] Iteration {i}: {response.status_code} {response.text}")

    print("\n--- Benchmark Results ---")
    print(f"Requests: {ITERATIONS}")
    print(f"Success: {success}/{ITERATIONS}")

    print(f"Min latency: {min(durations):.4f}s")
    print(f"Max latency: {max(durations):.4f}s")
    print(f"Avg latency: {statistics.mean(durations):.4f}s")
    print(f"P95 latency: {statistics.quantiles(durations, n=20)[-1]:.4f}s")


if __name__ == "__main__":
    run()