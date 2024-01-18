
FROM python:3.9 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

# Install wkhtmltopdf
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        libxrender1 \
        libxext6 \
        xfonts-75dpi \
        xfonts-base \
        wget \
        fontconfig \
        libjpeg62-turbo \
        xz-utils

RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb \
    && dpkg -i wkhtmltox_0.12.6-1.focal_amd64.deb \
    && apt-get install -f

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.9

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/

# Heroku uses PORT, Azure App Services uses WEBSITES_PORT, Fly.io uses 8080 by default
CMD ["sh", "-c", "uvicorn server.main:app --host 0.0.0.0 --port ${PORT:-${WEBSITES_PORT:-8080}}"]