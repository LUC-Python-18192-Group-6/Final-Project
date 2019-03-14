# from google.cloud import vision
# from google.cloud.vision import types
#
# client = vision.ImageAnnotatorClient()
# image = vision.types.Image()
# image.source.image_uri = 'gs://cloud-vision-codelab/eiffel_tower.jpg'
# resp = client.landmark_detection(image=image)
# print(resp.landmark_annotations)

# def implicit():
#     from google.cloud import storage
#
#     # If you don't specify credentials when constructing the client, the
#     # client library will look for credentials in the environment.
#     storage_client = storage.Client()
#
#     # Make an authenticated API request
#     buckets = list(storage_client.list_buckets())
#     print(buckets)

# Imports the Google Cloud client library
from google.cloud import storage

# Instantiates a client
storage_client = storage.Client()

# The name for the new bucket
bucket_name = 'my-new-bucket'

# Creates the new bucket
bucket = storage_client.create_bucket(bucket_name)

print('Bucket {} created.'.format(bucket.name))