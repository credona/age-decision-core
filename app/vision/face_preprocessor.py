import cv2
import numpy as np


class FacePreprocessor:
    """
    Prepares a cropped face image for the age estimation ONNX model.
    """

    def __init__(self, input_size: tuple[int, int] = (224, 224)):
        self.input_size = input_size

        self.mean = np.array([0.5, 0.5, 0.5], dtype=np.float32)
        self.std = np.array([0.5, 0.5, 0.5], dtype=np.float32)

    def preprocess(self, face_image) -> np.ndarray:
        """
        Convert a BGR cropped face to a normalized RGB NCHW tensor.
        """
        resized = cv2.resize(
            face_image,
            self.input_size,
            interpolation=cv2.INTER_AREA,
        )

        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

        normalized = rgb.astype(np.float32) / 255.0
        normalized = (normalized - self.mean) / self.std

        chw = np.transpose(normalized, (2, 0, 1))

        return np.expand_dims(chw, axis=0).astype(np.float32)