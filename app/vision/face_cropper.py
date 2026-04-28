class FaceCropper:
    """
    Extracts the main face region from the image.
    """

    def crop(self, image, faces):
        """
        Extract the first detected face.

        :param image: Original image (numpy array)
        :param faces: List of detected faces (x, y, w, h)
        :return: Cropped face image
        """
        if len(faces) == 0:
            raise ValueError("No face detected.")

        if len(faces) > 1:
            raise ValueError("Multiple faces detected.")

        x, y, w, h = faces[0]

        face = image[y : y + h, x : x + w]

        if face.size == 0:
            raise ValueError("Invalid face crop.")

        return face
