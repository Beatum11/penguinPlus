FROM python:3.10-slim

# setting environment
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . .

# starting
CMD ["python", "main.py"]