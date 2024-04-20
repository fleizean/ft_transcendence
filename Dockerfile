# Dockerfile
FROM python:alpine

ENV PIP_ROOT_USER_ACTION=ignore \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
    #PIP_NO_CACHE_DIR=off 

# Copy only requirements.txt first to leverage Docker cache
COPY requirements.txt /indianpong/requirements.txt

RUN pip install --upgrade pip && pip install -r /indianpong/requirements.txt

# After the packages are installed, copy the rest of your application
COPY indianpong /indianpong

RUN chmod +x /indianpong/start.sh

EXPOSE 8000

ENTRYPOINT ["sh", "/indianpong/start.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


