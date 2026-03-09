#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input --settings=icoportal.settings.prod

python manage.py migrate --settings=icoportal.settings.prod

