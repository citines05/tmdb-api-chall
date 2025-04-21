# Python official image
FROM python:3.10-slim

WORKDIR /app

COPY ./api ./api
COPY ./db ./db
COPY ./data ./data
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD python db/create_db.py && uvicorn api.main:app --host 0.0.0.0 --port 8000
