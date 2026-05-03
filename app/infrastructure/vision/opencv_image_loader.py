import cv2
import numpy as np


def load_image_from_bytes(image_bytes: bytes):
    """
    Decode uploaded image bytes into an OpenCV BGR image.
    """
    np_arr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError("Invalid image data.")

    return image
