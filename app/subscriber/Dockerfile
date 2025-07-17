FROM python:3.11-slim

RUN apt-get update && apt-get install -y

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-root

COPY . .

CMD ["poetry", "run", "python", "subscriber.py"]