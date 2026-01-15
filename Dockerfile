FROM python:3.13-bookworm

WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN pip install "poetry==2.2.1"
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false && poetry install --only main --no-interaction --no-ansi --no-root
COPY . /app

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
