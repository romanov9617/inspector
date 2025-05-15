#!/bin/sh
set -e

python admin/manage.py migrate
python admin/manage.py runserver 0.0.0.0:8000
