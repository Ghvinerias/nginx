FROM python:3.8

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --index-url https://pypi.org/simple --proxy http://squid-test.lb.ge:8080 -r requirements.txt

COPY . .

CMD ["python", "app/routes.py"]
