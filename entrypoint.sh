alembic upgrade head

pytest -v -p no:warnings 

uvicorn app.main:app --host 0.0.0.0 --port 8080