FROM python:3.14 AS builder
WORKDIR /app
COPY pyproject.toml .

RUN pip install --upgrade pip poetry poetry-plugin-export

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --with openstint --with mylaps --with web
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.14-slim
COPY --from=builder /app/wheels /wheels
ENV PYTHONDONTWRITEBYTECODE=1

RUN pip install --no-cache /wheels/* && rm -R /wheels

WORKDIR /app
COPY laptimes /app/laptimes
COPY rclaptimes /app/rclaptimes
COPY web /app/web
COPY *.py /app

CMD gunicorn