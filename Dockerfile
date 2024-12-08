FROM python:3.12.5-slim-bullseye

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install --no-dev

COPY . /app/

EXPOSE 8080

CMD ["sh", "-c", "python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8080"]