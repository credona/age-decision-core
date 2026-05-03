from typing import Any, Protocol

import numpy as np


class InputPreprocessorPort(Protocol):
    def preprocess(self, face_image: Any) -> np.ndarray: ...
