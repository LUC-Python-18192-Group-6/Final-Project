from random import choice
from PIL import Image, ImageDraw, ImageFont
import time
import json
import requests
from bs4 import BeautifulSoup
from google.cloud import vision
from google.oauth2 import service_account
from io import BytesIO
import sys

#User agents, important to make it seem as if we are accessing instagram through a browser
USER_AGENTS = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36']
#Inputting our credentials for the google API
credentials = service_account.Credentials.from_service_account_file('pythatjemet.json')
#Make an empty url lists and variables
counter = 0
progresscounter = 0
urls = []
labels = []
greenpics = []
green_labels = set(["Tree","Water","Grass","Mountain", "Ocean", "River", "Flower", "Animal", "Water sport", "Water transportation", "Nature", "Outdoors", "Outdoor", "Beach", "Fruit", "Leaf", "Leaves"])

print("Welcome to the Instagram account green score program! With this application you can check how green your favourite public account is!")

class InstagramScraper:
    def __init__(self, url, user_agents=None):
        self.url = url
        self.user_agents = user_agents
#Selecting a random agent to minimize being blocked
    def __random_agent(self):
        if self.user_agents and isinstance(self.user_agents, list):
            return choice(self.user_agents)
        return choice(USER_AGENTS)

    def __request_url(self):
        try:
            response = requests.get(
                self.url,
                headers={'User-Agent': self.__random_agent()})
            response.raise_for_status()
        except requests.HTTPError:
            raise requests.HTTPError('Received non-200 status code.')
        except requests.RequestException:
            raise requests.RequestException
        else:
            return response.text

    @staticmethod
    def extract_json(html):
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.find('body')
        script_tag = body.find('script')
        raw_string = script_tag.text.strip().replace('window._sharedData =', '').replace(';', '')
        return json.loads(raw_string)

    def page_metrics(self):
        results = {}
        try:
            response = self.__request_url()
            json_data = self.extract_json(response)
            metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']
        except Exception as e:
            raise e
        else:
            for key, value in metrics.items():
                if key != 'edge_owner_to_timeline_media':
                    if value and isinstance(value, dict):
                        value = value['count']
                        results[key] = value
        return results

    def post_metrics(self):
        results = []
        try:
            response = self.__request_url()
            json_data = self.extract_json(response)
            metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media'][
                'edges']
        except Exception as e:
            raise e
        else:
            for node in metrics:
                node = node.get('node')
                if node and isinstance(node, dict):
                    results.append(node)
        return results

def urlmaker():
    global url
    global post_metrics
    global instagram
    global instausername
    instausername = input("Please input instagram username:")
    #Define the URL for the profile page.
    url = 'https://www.instagram.com/{}'.format(instausername)
    # Initiate a scraper object and call one of the methods.
    instagram = InstagramScraper(url)
    post_metrics = instagram.post_metrics()
    if post_metrics != []:
        print("Great account choice, let's continue...")
    else:
        print("This account is set to private, try again!")
        urlmaker()
    # Fill the URL list
    for i in post_metrics:
        urls.append(i['display_url'])
        #labels.append(i['accessibility_caption'])

def urlcreation():
    try:
        urlmaker()
    except:
        print("This account does not exist, try again!")
        urlcreation()

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

#Then we run this function, which tries to obtain the list of urls. When we get an error (AKA the account doesnt exist, it will try again) if we dont, a variable named urls will be created.
urlcreation()

#Determining the 'green score' of the tested account
for i in urls:
    detect_labels(i)
    proglength = len(urls)
    lbs = set(lbs)
    labeltest = green_labels - lbs
    if len(labeltest) != len(green_labels):
        counter += 1
        greenpics.append(i)
    progresscounter +=1
    prgpercent = (progresscounter/proglength)*100
    sys.stdout.write("\rProgress: [" + "=" * (progresscounter) + " " * ((proglength - progresscounter)) + "]" + str(int(prgpercent)) + "%")
    sys.stdout.flush()
    # print("Progress: {}%  ".format(int(prgpercent)))

score = int((counter/len(urls))*100)
scoreprct = "The 'green score' of \n@{} \nis {}%!".format(instausername,score)

#Now we use the python PIL library to make a graphic about this account
shadowcolor = "black"
font123 = ImageFont.truetype("Phenomena-Regular.otf", 72)
resp123 = requests.get(greenpics[0])
img123 = Image.open(BytesIO(resp123.content))
image_size = img123.size
image_height = img123.size[1]
image_width = img123.size[0]
draw = ImageDraw.Draw(img123)
text_size = draw.textsize(scoreprct, font=font123)
wx = (image_width / 2) - (text_size[0] / 2)
hy = 0.9 * image_height -((image_height/3) - (text_size[1] / 3))
draw.text((wx - 1, hy - 1), scoreprct, font=font123, fill=shadowcolor, align='center')
draw.text((wx + 1, hy - 1), scoreprct, font=font123, fill=shadowcolor, align='center')
draw.text((wx - 1, hy + 1), scoreprct, font=font123, fill=shadowcolor, align='center')
draw.text((wx + 1, hy + 1), scoreprct, font=font123, fill=shadowcolor, align='center')
draw.multiline_text((wx, hy), scoreprct, (255, 255, 255), font=font123, align='center')
img123.show()

print("""\nThank you for using our Instagram account green scorer!
Written by Maarten Molenaar, Tom van Zantvliet and Sebastiaan Grosscurt
""")