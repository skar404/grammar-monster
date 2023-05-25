FROM python:3.11.3-buster

WORKDIR app/

# update pip and install poetry
RUN pip install -U pip && \
    pip install --no-cache-dir poetry

# install poetry packages
COPY ./poetry.lock .
COPY ./pyproject.toml .
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# copy code
COPY ./src .

USER 1001
CMD ["python", "main.py"]
