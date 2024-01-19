python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
		--display_name $DJANGO_SUPERUSER_DISPLAY_NAME

exec "$@"