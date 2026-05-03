from typing import Any, Protocol


class ImageDecoderPort(Protocol):
    def decode(self, image_bytes: bytes) -> Any: ...
