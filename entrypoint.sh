alembic upgrade head

pytest -sv -p no:warnings 

uvicorn app.main:app --host 0.0.0.0 --port 8080