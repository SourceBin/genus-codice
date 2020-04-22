import os
import pandas as pd

CURR_DIR = os.path.abspath(os.path.dirname(__file__))
DATASET_DIR = os.path.join(CURR_DIR, '../data/dataset')

def load():
  frames = []
  files = [x for x in os.listdir(DATASET_DIR) if x.endswith('.csv.gz')]

  for i, file in enumerate(files, start=1):
    print(f'{i}/{len(files)} - {file}')

    df = pd.read_csv(os.path.join(DATASET_DIR, file), converters={ 'content': str })
    frames.append(df)

  return pd.concat(frames)
