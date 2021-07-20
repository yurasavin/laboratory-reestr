FROM python:3.8.5-buster

ENV PYTHONUNBUFFERED 1

ENV TERM=xterm

COPY ./src /opt/app/src
COPY ./requirements.txt /opt/app/
COPY ./compose/django/entrypoint.sh /opt/app/
RUN pip install --upgrade pip && pip install --requirement /opt/app/requirements.txt

WORKDIR /opt/app/src
EXPOSE 8000

ENTRYPOINT ["/opt/app/entrypoint.sh"]
CMD /bin/sh -c "daphne --port 8000 --bind 0.0.0.0 conf.asgi:application"
