FROM python:3.12.0b1-bullseye

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./scripts/new.py .

CMD [ "python", "./worker.py" ]