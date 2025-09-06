from doc_processing.image_to_base64 import ImageToBase64
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

project_path = os.getenv("PROJECT_PATH")
IMAGE_PATH = Path(project_path + "/assets/unstructured/Image3.jpg")

if __name__ == "__main__":
    image = ImageToBase64(IMAGE_PATH)
    base64_data = image.base64_encode_image()
    print(base64_data)