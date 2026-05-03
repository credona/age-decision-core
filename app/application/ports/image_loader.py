from typing import Protocol

import numpy as np


class ImageLoaderPort(Protocol):
    def load(self, image_bytes: bytes) -> np.ndarray: ...
