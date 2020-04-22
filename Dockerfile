FROM python:3.6

WORKDIR /usr/src

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src src

CMD ["python3", "src/server.py"]
