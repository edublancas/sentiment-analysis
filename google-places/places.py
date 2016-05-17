# Get places ids
import yaml
import requests
import json
from tinydb import TinyDB

# Load key from yaml file
with open('key.yaml', 'r') as f:
    key = yaml.load(f.read())['google-key']

# load configuration parameters
with open('config.yaml', 'r') as f:
    config = yaml.load(f.read())

# Google maps API template
url_template = ('https://maps.googleapis.com/maps/api/place/radarsearch/json'
                '?key={key}&location={location}&radius={radius}&types={types}')

db = TinyDB('data/places.json')

# generate a request for every type of place
for a_type in config['types'].split('|'):
    # Parameters to be included in the request
    params = {'location': config['location'],
              'key': key,
              'radius': config['radius'],
              'types': a_type}
    
    # Make the request
    res = requests.get(url_template.format(**params))
    places = json.loads(res.content)['results']

    # Save results in a json file
    db.insert_multiple(places)
