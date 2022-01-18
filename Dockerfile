FROM python:3.8-slim-bullseye as build
COPY ./src /app
WORKDIR /app
RUN pip install pipenv==2022.1.8
RUN python -m venv .venv && \
    pipenv lock -r > requirements.txt && \
    . .venv/bin/activate && \
    pip install -r requirements.txt

FROM python:3.8-slim-bullseye
COPY --from=build /app /app
WORKDIR /app

ENV PORT=8080
# These are configured here for clarity. Will normally be overriden when running
ENV OIDC_ISSUER="http://localhost:${PORT}"
ENV OIDC_AUDIENCE="http://localhost:8082"

EXPOSE 8080

ENTRYPOINT .venv/bin/gunicorn "server:create_app()" -b "0.0.0.0:${PORT}"