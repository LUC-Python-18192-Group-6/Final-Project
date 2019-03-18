from google.cloud import vision
from google.cloud.vision import types
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import os
import io
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file('/Users/Tom/Python/Final-Project/pythatjemet.json')

# client = vision.ImageAnnotatorClient(credentials=credentials)
# image = vision.types.Image()
# image.source.image_uri = 'gs://cloud-vision-codelab/eiffel_tower.jpg'
# resp = client.landmark_detection(image=image)
# print(resp.landmark_annotations)

def detect_labels(path):
    """Detects labels in the file."""
    client = vision.ImageAnnotatorClient(credentials=credentials)

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')

    for label in labels:
        print(label.description)

detect_labels('IMG_2299.jpg')