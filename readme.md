# Procno backend

# Initialtion

### Start the environment:
```shell
poetry install
poetry shell
```
### Create tables and add example data:
```shell
cd tools
python add_sample_data.py
```

### Run the backend:
```bash
#alembic upgrade head
# init first start
#python app/backend_pre_start.py
#python app/initial_data.py

# start the server
uvicorn app.main:app --host 0.0.0.0 --port 8888
uvicorn app.main:app --reload --host 0.0.0.0 --port 8888 --ssl-keyfile=../localhost+2-key.pem --ssl-certfile=../localhost+2.pem
```

BIG TODO:
- Migration using Alembic. For now, stick with plain SQL.

## Some helper SQL
```sql
-- Count topics of users
select owner_uniq_id, count(id) counted from topics group by topics.owner_uniq_id order by counted desc 

```

```bash
# Use text to speech for testing
sudo apt install ffmpeg espeak
```