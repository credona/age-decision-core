from typing import Any, Protocol


class FaceCropperPort(Protocol):
    def crop(self, image: Any, faces: list) -> Any: ...
