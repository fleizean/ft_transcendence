FROM python:3.11.4-slim-buster

WORKDIR /ft_transcendence

ENV PIP_ROOT_USER_ACTION=ignore

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
COPY ./renewdb.sh .
COPY ./localhost.crt .
COPY ./localhost.key .
RUN chmod +x /ft_transcendence/renewdb.sh
###
EXPOSE 8001

CMD ["sh", "/ft_transcendence/renewdb.sh"]

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]