import re

def normalize_content(content):
  content = re.sub(r'(\w+)', r' \1 ', content)
  content = content.lower()
  return content
