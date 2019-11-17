#!/bin/bash
# Set strict mode options
set -euo pipefail

# Set default value for the server
DEFAULT="webserver"
SERVER=${1:-$DEFAULT}

# Set a default value for production status
PRODUCTION=${IN_PRODUCTION:-0}

if [ "$PRODUCTION" = 0 ]; then
    # continue only if database is up (local only)
    printf "%s" "waiting for database ..."
    while ! ping -c 1 -n -w 1 db &> /dev/null
    do
        printf "%c" "."
    done
    printf "\n%s\n"  "Database is online!"
fi

if [ "$SERVER" = "webserver" ]; then
    echo "Starting Django server"
    cd streetteam
    python manage.py migrate
    python manage.py collectstatic --no-input

    if [ "$PRODUCTION" = 1 ]; then
        # TODO remove --reload once we move to image
        gunicorn "streetteam.wsgi" -b 0.0.0.0:8100 --reload --env DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}
    elif [ "$PRODUCTION" = 0 ]; then
        gunicorn "streetteam.wsgi" -b 0.0.0.0:8100 --reload --timeout 100000 --env DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}
    else
        echo "Unrecognized option for variable IN_PRODUCTION: '$PRODUCTION'"
        exit 1
    fi
elif [ "$SERVER" = "worker" ]; then
    echo "TODO Starting Celery worker"
else
    echo "Unrecognized option for server: '$SERVER'"
    exit 1
fi
