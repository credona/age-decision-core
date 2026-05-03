from typing import Protocol

import numpy as np


class InputAnalyzerPort(Protocol):
    def get_status(self) -> dict: ...

    def detect(self, image: np.ndarray) -> list: ...
