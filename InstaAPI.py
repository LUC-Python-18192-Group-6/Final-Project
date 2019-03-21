from random import choice
import json
import requests
from bs4 import BeautifulSoup
from google.cloud import vision
from google.oauth2 import service_account
import turtle

#User agents, important to make it seem as if we are accessing instagram through a browser
USER_AGENTS = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36']
#Inputting our credentials for the google API
credentials = service_account.Credentials.from_service_account_file('/Users/Tom/Python/Final-Project/pythatjemet.json')
#Make an empty url lists and variables
counter = 0
urls = []
labels = []
greenpics = []
green_labels = set(["Tree","Water","Grass","Mountain", "Ocean", "River", "Flower", "Animal", "Water sport", "Water transportation", "Nature", "Outdoors", "Outdoor", "Beach", "Fruit"])

print("Welcome to the Instagram green scorer!")

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
    lbs = set(lbs)
    labeltest = green_labels - lbs
    if len(labeltest) != len(green_labels):
        counter += 1
        greenpics.append(i)

score = int((counter/len(urls))*100)
scoreprct = "Your 'green score' is {}%".format(score)
print(scoreprct)
print(greenpics)
#TURTLE TIMEEEEE
