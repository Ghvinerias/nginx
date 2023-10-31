FROM python:3.10-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir requirements.txt

COPY ./worker.py .

CMD [ "python", "./worker.py" ]