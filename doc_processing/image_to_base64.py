import base64

class ImageToBase64():
    def __init__(self, image_path):
        self.image_path = image_path

    def base64_encode_image(self):
        with open(self.image_path, "rb") as image_file:
            image_bytes = image_file.read()
            base64_bytes = base64.b64encode(image_bytes).decode('utf-8')
            return base64_bytes


