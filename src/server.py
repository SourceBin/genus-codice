import os
import json
import joblib
from flask import Flask, request, jsonify

CURR_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join('../data')

app = Flask(__name__)

print('Loading model')
model = joblib.load(os.path.join(DATA_DIR, 'model.gz'))

print('Loading languages')
with open(os.path.join(DATA_DIR, 'languages.json')) as f:
  languages = list(json.load(f).keys())

@app.route('/languages')
def get_languages():
  return jsonify(languages)

@app.route('/classify', methods=['POST'])
def classify():
  return jsonify(list(model.predict(request.json)))
