#Importing libraries
from google.cloud import vision
from google.cloud.vision import types
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import os
import io
from google.oauth2 import service_account

#Inputting our credentials for the google API
credentials = service_account.Credentials.from_service_account_file('/Users/Tom/Python/Final-Project/pythatjemet.json')

#Defining our empty variables:
counter = 0

#Defining our function that interacts with the google API
def detect_labels(path):
    """Detects labels in the file."""
    global lbs
    lbs = []
    client = vision.ImageAnnotatorClient(credentials=credentials)

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    for label in labels:
        lbs.append(label.description)


#Appending the received labels to our empty list
detect_labels('foto.jpg')
print(lbs)

#Changing it to a set, so we can do relevant operations.
lbs = set(lbs)

#Our set of test labels:
green_labels = set(["Tree","Water","Grass","Mountain", "Ocean", "River", "Flower", "Animal"])

#Our test goes as follows
labeltest = green_labels - lbs


if len(labeltest) != len(green_labels):
    counter += 1

# score = (counter / len(image_list))*100


print(counter)
