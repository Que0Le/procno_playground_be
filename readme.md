


Run without docker:

```bash
poetry install
poetry shell

alembic upgrade head
# init first start
python app/backend_pre_start.py
python app/initial_data.py

# start the server
uvicorn app.main:app --host 0.0.0.0 --port 8888
```

BIG TODO:
- Migration using Alembic. For now, stick with plain SQL.
