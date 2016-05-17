# load reviews in json file and convert them to a format suitable for
# further processing
from tinydb import TinyDB
import pandas as pd

db = TinyDB('data/reviews.json')

# function designed to assign labels to each review
# for now we are only taking the overall rating which
# has a value between 1 and 5
def label_review(review):
    rating = review['rating']

    if rating <= 2:
        return 0
    elif rating == 3:
        return None
    else:
        return 1

rows = []
for i in xrange(1, len(db)):
    review = db.get(eid=i)
    label = label_review(review)
    content = review['text'].encode('utf-8')
    rows.append((content, label))

df = pd.DataFrame(rows, columns=['content', 'label'])
df.to_csv('data/reviews.csv', index=False)
