#!/bin/sh
source venv/bin/activate
flask db upgrade
# flask translate compile
exec gunicorn --statsd-host=localhost:9125 --statsd-prefix=microblog -b :5000 --access-logfile - --error-logfile - microblog:app
