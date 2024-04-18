#!/bin/bash

cd indianpong
python3 manage.py makemigrations pong
python3 manage.py migrate
python3 manage.py initdata
python3 manage.py populate 10
python3 manage.py collectstatic --no-input
echo "Starting Daphne server..."
daphne -b 0.0.0.0 -p 8001 -e ssl:8443:privateKey=/etc/nginx/ssl/key.pem:certKey=/etc/nginx/ssl/cert.pem indianpong.asgi:application
echo "Daphne server started"