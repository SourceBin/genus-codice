import os
import json

CURR_DIR = os.path.abspath(os.path.dirname(__file__))

query = r'''WITH
  languages AS (
  SELECT
    files.id,
    RAND() AS random,
    -- this regex extracts the extension, or final part of a path
    -- a/b/c        -> c
    -- a/b/c.py     -> .py
    -- a/b/c.py.txt -> .txt
    CASE REGEXP_EXTRACT(files.path, r'(\.?[^\/\.]*)$')
{}
    END
      AS lang
  FROM
    `bigquery-public-data.github_repos.files` AS files
  ORDER BY
    random), -- randomly order the dataset

  row_numbers AS (
  SELECT
    languages.id,
    languages.lang,
    -- assign row numbers to every row grouped by language
    -- this makes it possible to select n rows per language
    ROW_NUMBER() OVER (PARTITION BY languages.lang) AS row_number
    FROM languages)

SELECT
  contents.content,
  row_numbers.lang
FROM
  row_numbers
INNER JOIN
  `bigquery-public-data.github_repos.contents` AS contents
ON
  contents.id = row_numbers.id
WHERE
  (row_numbers.lang IS NOT NULL)
  AND
  (row_numbers.row_number <= 10000) -- only select 10k rows per language
  AND
  (contents.content IS NOT NULL);
'''

with open(os.path.join(CURR_DIR, '../data/languages.json')) as f:
  languages = json.load(f)

matches = []

for language, value in languages.items():
  if 'filenames' in value:
    for filename in value['filenames']:
      matches.append((filename, language))

  for extension in value['extensions']:
    matches.append((f'.{extension}', language))

max_len = len(max(matches, key=lambda x: len(x[0]))[0])

whens = [
  f'      WHEN \'{match[0]}\' {" " * (max_len - len(match[0]))} THEN \'{match[1]}\''
  for match in matches
]

with open(os.path.join(CURR_DIR, 'bigquery_github_query.sql'), 'w') as f:
  f.write(query.format('\n'.join(whens)))
