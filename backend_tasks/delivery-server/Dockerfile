FROM python:3.10-slim AS build
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes gcc libpython3-dev && \
    python -m venv /venv && \
    /venv/bin/pip install --upgrade pip

# Build the virtualenv as a separate step: Only re-execute this step when requirements.txt changes
FROM build AS base-venv
COPY requirements.txt /requirements.txt
RUN /venv/bin/pip install --disable-pip-version-check -r /requirements.txt

FROM base-venv AS build-venv
ENV PATH="/venv/bin:$PATH"
COPY pyproject.toml /pyproject.toml
COPY poetry.lock /poetry.lock
RUN  poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

FROM python:3.10-slim
COPY --from=build-venv /venv /venv
ENV PATH="/venv/bin:$PATH"
COPY . /app
WORKDIR /app
ENTRYPOINT ["gunicorn","-b","0.0.0.0:8000"]
