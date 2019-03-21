#Importing libraries
from google.cloud import vision
from google.oauth2 import service_account

#Inputting our credentials for the google API
credentials = service_account.Credentials.from_service_account_file('/Users/Tom/Python/Final-Project/pythatjemet.json')

#Defining our empty variables:
counter = 0

#Defining our function that interacts with the google API
def detect_labels(uri):
    """Detects labels in the file."""
    global lbs
    lbs = []
    client = vision.ImageAnnotatorClient(credentials=credentials)

    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.label_detection(image=image)
    labels = response.label_annotations

    for label in labels:
        lbs.append(label.description)

#Appending the received labels to our empty list
detect_labels("https://scontent-amt2-1.cdninstagram.com/vp/a6bc2bb26acd3ebd4c108b10d913aeb6/5D1F6A47/t51.2885-15/e35/12093572_1558187451158171_1674724162_n.jpg?_nc_ht=scontent-amt2-1.cdninstagram.com")
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
