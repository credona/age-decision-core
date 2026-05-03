from typing import Protocol

import numpy as np


class InferenceEnginePort(Protocol):
    def get_status(self) -> dict: ...

    def predict(self, prepared_input: np.ndarray) -> tuple[float, float]: ...
