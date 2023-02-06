
FROM python:3.11-slim-bullseye

# Set environment variables.
ENV PYTHONWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
ENV POETRY_VERSION 1.3.2
ENV GRPC_PYTHON_BUILD_SYSTEM_ZLIB 1

# Install dependencies.
RUN pip install "poetry==$POETRY_VERSION"

# Set working directory.
WORKDIR /code

# Copy dependencies.
COPY poetry.lock pyproject.toml /code/

# Project init
RUN POETRY_VIRTUALENVS_CREATE=false poetry install --only main --no-interaction --no-ansi --no-root

# Copy project.
COPY . /code/

EXPOSE 8080

ENTRYPOINT [ "gunicorn", "app.main:app", "--workers", "2", "--worker-class", \
        "uvicorn.workers.UvicornWorker",  "-b", "0.0.0.0:8080" ]
