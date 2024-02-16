FROM python:3.11.4-slim-buster

WORKDIR /ft_transcendence

ENV PIP_ROOT_USER_ACTION=ignore

COPY requirements.txt .

RUN python -m venv venv
RUN . venv/bin/activate
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
#run pip install --root-user-action=ignore
COPY . .
COPY ./renewdb.sh .
RUN chmod +x /ft_transcendence/renewdb.sh
###
EXPOSE 8000

ENTRYPOINT ["sh", "/ft_transcendence/renewdb.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]