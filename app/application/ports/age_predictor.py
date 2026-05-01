from typing import Protocol

import numpy as np


class AgePredictorPort(Protocol):
    def get_status(self) -> dict: ...

    def predict(self, face_tensor: np.ndarray) -> tuple[float, float]: ...
