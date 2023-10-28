FROM python:3.8-alpine

WORKDIR /app

COPY . .

RUN apk add --no-cache --virtual .build-deps gcc musl-dev

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]