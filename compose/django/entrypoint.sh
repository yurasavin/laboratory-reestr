#!/bin/bash

python /opt/app/src/manage.py migrate
python /opt/app/src/manage.py collectstatic --noinput

exec "$@"