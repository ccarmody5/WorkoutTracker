FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt .
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libc6-dev libpq-dev libpq5 \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove gcc libc6-dev libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --system --no-create-home workout \
    && install -d -o workout /app/logs

COPY alembic.ini webapp.py terminal_program.py ./
COPY alembic/ alembic/
COPY config/ config/
COPY docker/ docker/
COPY helpers/ helpers/
COPY static/ static/
COPY templates/ templates/
USER workout
EXPOSE 5000
CMD ["sh", "-c", "alembic upgrade head && python -m docker.bootstrap && exec flask --app webapp:webapp run --host=0.0.0.0 --without-threads"]
