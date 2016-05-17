# Load places data and get reviews for each one
import requests
import json
from tinydb import TinyDB
import yaml

# load places
places_db = TinyDB('data/places.json')
# load database to store reviews
reviews_db = TinyDB('data/reviews.json')

# Load key from yaml file
with open('key.yaml', 'r') as f:
    key = yaml.load(f.read())['google-key']

# load language parameter
with open('config.yaml', 'r') as f:
    language = yaml.load(f.read())['language']

# template url used to send requests
url_template = ('https://maps.googleapis.com/maps/api/place/details/json?'
                'key={key}&placeid={placeid}&language={language}')

# load details for every place
for i in xrange(1, len(places_db)):
    # build dic with params to send to the API
    params = {'key': key,
              'placeid': places_db.get(eid=i)['place_id'],
              'language': language}
    # send request
    res = requests.get(url_template.format(**params))
    # obtain reviews if any
    try:
        reviews = json.loads(res.content)['result']['reviews']
    except Exception, e:
        print 'Place does not have reviews, skipping...'
    else:
        # insert reviews in json file
        reviews_db.insert_multiple(reviews)
