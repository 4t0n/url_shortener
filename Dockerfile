FROM python:3.11 AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sSLo /app/wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && \
chmod +x /app/wait-for-it.sh

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /app

ENV PYTHONPATH=/app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY alembic /app/alembic
COPY alembic.ini .
COPY tests /app/tests
COPY app /app/app
COPY main.py /app/
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

COPY --from=builder /app/wait-for-it.sh /app/wait-for-it.sh

CMD ["/app/entrypoint.sh"]
