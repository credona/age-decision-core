from app.infrastructure.vision.opencv_image_loader import load_image_from_bytes


class OpenCvImageDecoder:
    """
    Decodes image bytes using the production OpenCV image loader.
    """

    def decode(self, image_bytes: bytes):
        return load_image_from_bytes(image_bytes)
