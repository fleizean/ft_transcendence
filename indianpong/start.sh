python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
		--display_name $DJANGO_SUPERUSER_DISPLAY_NAME
python3 manage.py indianai
exec "$@"
