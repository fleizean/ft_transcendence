# Dockerfile
FROM python:3.11.4-slim-buster

ENV PIP_ROOT_USER_ACTION=ignore \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
    #PIP_NO_CACHE_DIR=off 


COPY indianpong /indianpong

RUN pip install --upgrade pip && pip install -r /indianpong/requirements.txt

RUN chmod +x /indianpong/start.sh

EXPOSE 8001

CMD [ "bash", "/indianpong/start.sh" ]


