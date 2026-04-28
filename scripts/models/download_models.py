from pathlib import Path
from urllib.request import urlretrieve

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


def download_file(target_path: str, url: str) -> None:
    path = Path(target_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        print(f"Already exists: {target_path}")
        return

    print(f"Downloading: {target_path}")
    urlretrieve(url, path)
    print(f"Saved: {target_path}")


def main() -> None:
    for target_path, url in MODELS.items():
        download_file(target_path, url)


if __name__ == "__main__":
    main()
