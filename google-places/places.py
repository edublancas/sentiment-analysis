# Get places ids
import yaml
import requests
import json
from tinydb import TinyDB

# Load key from yaml file
with open('config.yaml', 'r') as f:
    key = yaml.load(f.read())['google-key']

# Google maps API template
url_template = ('https://maps.googleapis.com/maps/api/place/radarsearch/json'
                '?key={key}&location={location}&radius={radius}&types={types}')

# Parameters to be included in the request
params = {'location': '19.4154733,-99.1296775',
          'key': key,
          'radius': '50000',
          'types': 'food'}

# Make the request
res = requests.get(url_template.format(**params))
places = json.loads(res.content)['results']

# Save results in a json file
db = TinyDB('places.json')
db.insert_multiple(places)
