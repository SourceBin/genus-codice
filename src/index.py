import re
import dataset

from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

print('Loading dataset')
data = dataset.load()
print(data)
print(data.groupby('lang').size())

print('Building pipeline')
pipeline = Pipeline(steps=[
  ('tfidf', TfidfVectorizer(token_pattern=r'\w+|[^\w\s]+')),
  ('random_forest', RandomForestClassifier(verbose=2, n_jobs=-1)),
])

print('Splitting data')
x_train, x_test, y_train, y_test = train_test_split(data['content'], data['lang'], test_size=0.2)

print('Fitting model')
pipeline.fit(x_train, y_train)

print('Predicting model')
preds = pipeline.predict(x_test)

print('Measuring accuracy')
score = accuracy_score(y_test, preds)
print(score)
