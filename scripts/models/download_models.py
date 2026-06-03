import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

MODELS = {
    "models/face_detection/face_detection_yunet_2023mar.onnx": (
        "https://github.com/opencv/opencv_zoo/raw/main/models/"
        "face_detection_yunet/face_detection_yunet_2023mar.onnx"
    ),
    "models/age_estimation/age-gender-prediction-ONNX.onnx": (
        "https://huggingface.co/onnx-community/age-gender-prediction-ONNX/"
        "resolve/main/onnx/model.onnx"
    ),
}

MAX_ATTEMPTS = 5
TIMEOUT_SECONDS = 60


def download_file(target_path: str, url: str) -> None:
    path = Path(target_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists() and path.stat().st_size > 0:
        print(f"Already exists: {target_path}")
        return

    last_error: Exception | None = None

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            print(f"Downloading: {target_path} (attempt {attempt}/{MAX_ATTEMPTS})")
            request = Request(
                url,
                headers={
                    "User-Agent": "age-decision-core-ci-model-downloader/2.6.0",
                },
            )

            with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
                path.write_bytes(response.read())

            print(f"Saved: {target_path}")
            return

        except (HTTPError, URLError, TimeoutError) as exc:
            last_error = exc
            if path.exists():
                path.unlink()

            if attempt == MAX_ATTEMPTS:
                break

            sleep_seconds = attempt * 10
            print(f"Download failed: {target_path}. Retrying in {sleep_seconds}s.")
            time.sleep(sleep_seconds)

    raise RuntimeError(f"Failed to download model file: {target_path}") from last_error


def main() -> None:
    for target_path, url in MODELS.items():
        download_file(target_path, url)


if __name__ == "__main__":
    main()
