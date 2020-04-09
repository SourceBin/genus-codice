import os
import json

DATASET_FILE = 'dataset.json'

LANGUAGES = [
    'JavaScript',
    'Python',
    'Java',
    'Kotlin',
    'PHP',
    'C++',
    'TypeScript',
    'Haskell',
    'Lisp',
    'Clojure',
    'PowerShell',
    'Ruby',
    'Scala',
    'Swift',
    'CoffeeScript',
    'Go',
    'R',
    ### 'C-sharp',
    ### 'UNIX-Shell',
    ### 'X86-Assembly',
    ### 'Objective-C',
]

def get_files(language):
    print(f'Loading {language} files')

    dirs = [x[0]
        for x in os.walk(f'RosettaCodeData/Task')
        if x[0].endswith(language)]

    files = []
    for dir in dirs:
        for file in os.listdir(dir):
            files.append(f'{dir}/{file}')

    print(f'Finished loading {language} files')
    return files

def create():
    print('Creating dataset')
    dataset = []

    for language in LANGUAGES:
        for file in get_files(language):
            with open(file) as f:
                dataset.append([f.read(), language])

    print(f'Loaded {len(dataset)} files from {len(LANGUAGES)} languages')
    print('Finished creating dataset')
    return dataset

def load():
    if os.path.isfile(DATASET_FILE):
        with open(DATASET_FILE) as f:
            return json.load(f)
    else:
        dataset = create()
        with open(DATASET_FILE, 'w') as f:
            json.dump(dataset, f)
            return dataset
