#!/bin/bash

/app/wait-for-it.sh $DATABASE_HOST:5432 --timeout=60 --strict -- echo "Database is up"
/app/wait-for-it.sh $TEST_DATABASE_HOST:5432 --timeout=60 --strict -- echo "Database is up"

echo "Waiting 5 sec..."
sleep 5

echo "Starting Migrations..."
alembic -c /app/alembic.ini revision --autogenerate -m "alembic_migration" || echo "No changes in models, skipping migration."
echo "Starting Migrations for Main Database..."
DATABASE_URL=$DATABASE_URL alembic upgrade head || echo "No changes in models, skipping migration."

echo "Starting Migrations for Test Database..."
DATABASE_URL=$TEST_DATABASE_URL alembic upgrade head || echo "No changes in models, skipping migration."


echo "Starting tests..."
pytest tests/
TEST_EXIT_CODE=$?

echo "Starting url_shortener app..."
exec uvicorn main:app --host 0.0.0.0 --port 80
