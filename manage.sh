#!/usr/bin/env bash
SCRIPT_DIRECTORY="$(dirname "$BASH_SOURCE")"

docker compose -f ${SCRIPT_DIRECTORY}/docker-compose.yml exec web python /app/manage.py "$@"
