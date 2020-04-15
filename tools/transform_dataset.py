import os
import io
import json
import pandas as pd

DATA_DIR = 'data'
LANGUAGES_FILE = os.path.join(DATA_DIR, 'languages.json')
DATASET_SRC = os.path.join(DATA_DIR, 'source')
DATASET_OUT = os.path.join(DATA_DIR, 'dataset')

with open(LANGUAGES_FILE) as f:
  languages = json.load(f)

filenames = dict([
  (filename, language)
  for language in languages.keys()
  if 'filenames' in languages[language]
  for filename in languages[language]['filenames']
])

extensions = dict([
  (ext, language)
  for language in languages.keys()
  for ext in languages[language]['extensions']
])

def get_language_from_row(row):
  filename_ext = os.path.basename(row.sample_path)
  filename, ext = os.path.splitext(filename_ext)

  if filename in filenames:
    return filenames[filename]
  elif ext in extensions:
    return extensions[ext]
  else:
    return None

def transform_file(file):
  df = pd.read_csv(file)
  df = df.filter(['content', 'sample_path'])
  df = df[df.content.notnull()]
  df['language'] = df.apply(lambda row: get_language_from_row(row), axis=1)
  df = df[df.language.notnull()]
  return df

files = [x for x in os.listdir(DATASET_SRC) if x.endswith('.csv.gz')]
print(f'Transforming {len(files)} files')

for i, filename in enumerate(files, start=1):
  print(f'{i}/{len(files)} - {filename}')
  file = os.path.join(DATASET_SRC, filename)
  df = transform_file(file)
  df.to_csv(os.path.join(DATASET_OUT, filename))
