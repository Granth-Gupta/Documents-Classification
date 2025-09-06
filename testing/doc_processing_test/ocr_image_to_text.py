from OCR.imagetoText import ocr_readable
from dotenv import load_dotenv
import os

load_dotenv()

project_path = os.getenv("PROJECT_PATH")
IMAGE_PATH = project_path + "/assets/unstructured/Image3.jpg"

if __name__ == "__main__":
    texts = ocr_readable(IMAGE_PATH)
    print(texts)

# OUTPUT
# Our Roadmap for Web Development Projects This slide shows the roadmap for web development setup in the organization and what actions to be made at each stage after some time_
# Decide Which services are best for you according your needs
# Planning We decide on functionality of the website outline of pages content creation of sitemaps
# Development We build the chosen visual design until we satisfy with the look of the website
# Website Development We write codes for website working and content formatting
# Launch After approval from You launch the website
# 060 eig
# Discuss Discuss the project requirements your business objectives your clients customer and goals
# Visual Design Explore possible visual designs using static mock-ups
# Framework Development this stage we build framework for the website and hierarchy in which the content would be represented
# Testing We checkthe functionality of the website on multiple device
# This slide Is 100%0 editable Adapt it t your needs and capture your audience attention