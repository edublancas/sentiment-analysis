import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.linear_model import SGDClassifier

df = pd.read_csv('../google-places/data.csv')

# keep columns that have content and label
df = df[df.content.notnull() & df.label.notnull()]

# remove duplicates
df  = df[~df.duplicated()]


# build a scikit-learn pipeline for text classification
text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', SGDClassifier(loss='hinge',
                                           penalty='l2',
                                           alpha=1e-3,
                                           n_iter=5,
                                           random_state=42))])

# grid search parameters
parameters = {'vect__ngram_range': [(1, 1), (1, 2)],
              'tfidf__use_idf': (True, False),
              'clf__alpha': (1e-2, 1e-3)}

# train
gs_clf = GridSearchCV(text_clf, parameters, n_jobs=-1)
gs_clf = gs_clf.fit(df.content.values, df.label.values)