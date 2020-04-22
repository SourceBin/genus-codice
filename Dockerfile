FROM python:3.6

WORKDIR /usr/src

EXPOSE 5000

ENV FLASK_APP "src/server.py"

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY data data
COPY src src

CMD ["gunicorn", "--chdir", "src", "--bind", "0.0.0.0:5000", "server:app"]
