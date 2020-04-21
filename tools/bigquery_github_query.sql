WITH
  languages AS (
  SELECT
    files.id,
    RAND() AS random,
    -- this regex extracts the extension, or final part of a path
    -- a/b/c        -> c
    -- a/b/c.py     -> .py
    -- a/b/c.py.txt -> .txt
    CASE REGEXP_EXTRACT(files.path, r'(\.?[^\/\.]*)$')
      WHEN '.js'          THEN 'JavaScript'
      WHEN '.cjs'         THEN 'JavaScript'
      WHEN '.ts'          THEN 'TypeScript'
      WHEN '.java'        THEN 'Java'
      WHEN '.py'          THEN 'Python'
      WHEN '.kt'          THEN 'Kotlin'
      WHEN '.ktm'         THEN 'Kotlin'
      WHEN '.kts'         THEN 'Kotlin'
      WHEN '.c'           THEN 'C'
      WHEN '.h'           THEN 'C'
      WHEN '.c++'         THEN 'C++'
      WHEN '.cpp'         THEN 'C++'
      WHEN '.h++'         THEN 'C++'
      WHEN '.hpp'         THEN 'C++'
      WHEN '.cs'          THEN 'C#'
      WHEN '.erl'         THEN 'Erlang'
      WHEN '.ex'          THEN 'Elixir'
      WHEN '.exs'         THEN 'Elixir'
      WHEN '.hs'          THEN 'Haskell'
      WHEN '.go'          THEN 'Go'
      WHEN '.php'         THEN 'PHP'
      WHEN '.rb'          THEN 'Ruby'
      WHEN '.rs'          THEN 'Rust'
      WHEN '.scala'       THEN 'Scala'
      WHEN '.swift'       THEN 'Swift'
      WHEN '.lisp'        THEN 'Common Lisp'
      WHEN '.clj'         THEN 'Clojure'
      WHEN '.r'           THEN 'R'
      WHEN '.matlab'      THEN 'MATLAB'
      WHEN '.m'           THEN 'MATLAB'
      WHEN '.asm'         THEN 'Assembly'
      WHEN '.nasm'        THEN 'Assembly'
      WHEN '.d'           THEN 'D'
      WHEN '.dart'        THEN 'Dart'
      WHEN '.jl'          THEN 'Julia'
      WHEN '.groovy'      THEN 'Groovy'
      WHEN '.hx'          THEN 'Haxe'
      WHEN '.lua'         THEN 'Lua'
      WHEN '.sh'          THEN 'Shell'
      WHEN '.bash'        THEN 'Shell'
      WHEN '.ps1'         THEN 'PowerShell'
      WHEN '.psd1'        THEN 'PowerShell'
      WHEN '.psm1'        THEN 'PowerShell'
      WHEN '.sql'         THEN 'SQL'
      WHEN 'Dockerfile'   THEN 'Dockerfile'
      WHEN '.dockerfile'  THEN 'Dockerfile'
      WHEN '.md'          THEN 'Markdown'
      WHEN '.markdown'    THEN 'Markdown'
      WHEN '.mdown'       THEN 'Markdown'
      WHEN '.html'        THEN 'HTML'
      WHEN '.htm'         THEN 'HTML'
      WHEN '.css'         THEN 'CSS'
      WHEN '.sass'        THEN 'Sass'
      WHEN '.scss'        THEN 'SCSS'
      WHEN '.vue'         THEN 'Vue'
      WHEN '.json'        THEN 'JSON'
      WHEN '.yml'         THEN 'YAML'
      WHEN '.yaml'        THEN 'YAML'
      WHEN '.xml'         THEN 'XML'
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
