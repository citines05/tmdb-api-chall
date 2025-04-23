# Python official image
FROM 3.11-slim

WORKDIR /app

COPY ./api ./api
COPY ./db ./db
COPY ./data ./data
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD python data/clean_movies.py && python db/create_db.py && uvicorn api.main:app --host 0.0.0.0 --port 8000
