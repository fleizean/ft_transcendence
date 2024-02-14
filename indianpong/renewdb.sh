#!/bin/bash

# Delete all files except "__init__.cpython-310.pyc" in all "__pycache__" directories
find . -path '*/__pycache__/*' ! -name '__init__.cpython-310.pyc' -type f -delete

# Delete all files except "__init__.py" in all "migrations" directories
find . -path '*/migrations/*' ! -name '__init__.py' -type f -delete

# Delete db.sqlite3
rm -f db.sqlite3

# Execute Django management commands
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py superuser
python3 manage.py indianai
python3 manage.py loaddata store_data