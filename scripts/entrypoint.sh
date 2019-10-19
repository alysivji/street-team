#!/bin/bash
# Set strict mode options
set -euo pipefail

# Set default value for the server
DEFAULT="webserver"
SERVER=${1:-$DEFAULT}

# Set a default value for production status
PRODUCTION=${IN_PRODUCTION:-0}

# continue only if database is up
printf "%s" "waiting for database ..."
while ! ping -c 1 -n -w 1 db &> /dev/null
do
    printf "%c" "."
done
printf "\n%s\n"  "Database is online!"

if [ "$SERVER" = "webserver" ]; then
    echo "Starting Django server"
    python streetteam/manage.py migrate
    python streetteam/manage.py runserver 0.0.0.0:8000
elif [ "$SERVER" = "worker" ]; then
    echo "TODO Starting Celery worker"
else
    echo "Unrecognized option for server: '$SERVER'"
    exit 1
fi
