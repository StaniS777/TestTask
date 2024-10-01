#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for database..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.2
    done

    echo "Database SQL started"
fi

python manage.py migrate

exec "$@"
