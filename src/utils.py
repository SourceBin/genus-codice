import re

CHUNK_SIZE = 2048

def normalize_content(content):
  chunks = []

  for chunk in range(0, len(content), CHUNK_SIZE):
    x = content[chunk:chunk + CHUNK_SIZE]
    x = re.sub(r'(\w+)', r' \1 ', x)
    x = x.lower()
    chunks.append(x)

  return chunks
