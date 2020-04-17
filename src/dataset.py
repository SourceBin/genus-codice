import os
import pandas as pd

DATASET_DIR = 'data/dataset'

def load():
  frames = []
  files = [x for x in os.listdir(DATASET_DIR) if x.endswith('.csv.gz')]
  files = [files[0]] # TODO: remove

  for i, file in enumerate(files, start=1):
    print(f'{i}/{len(files)} - {file}')

    df = pd.read_csv(os.path.join(DATASET_DIR, file), converters={ 'content': str })
    frames.append(df)

  return pd.concat(frames)
