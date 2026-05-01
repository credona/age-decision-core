import os

import cv2

from app.infrastructure.config.settings import settings


class FaceDetector:
    """
    Detects faces using the YuNet ONNX face detector.
    """

    def __init__(self):
        self.model_path = settings.face_detection_model_path

        if not os.path.exists(self.model_path):
            raise RuntimeError(f"Face detection model not found: {self.model_path}")

        self.detector = cv2.FaceDetectorYN.create(
            model=self.model_path,
            config="",
            input_size=(320, 320),
            score_threshold=0.6,
            nms_threshold=0.3,
            top_k=5000,
        )

    def detect(self, image):
        """
        Detect faces and return bounding boxes as (x, y, w, h).
        """
        height, width = image.shape[:2]

        self.detector.setInputSize((width, height))

        _, faces = self.detector.detect(image)

        if faces is None:
            return []

        boxes = []

        for face in faces:
            x, y, w, h = face[:4]

            boxes.append(
                (
                    max(0, int(x)),
                    max(0, int(y)),
                    int(w),
                    int(h),
                )
            )

        return boxes

    def get_status(self) -> dict:
        return {
            "model": "YuNet",
            "model_path": self.model_path,
            "loaded": self.detector is not None,
        }
