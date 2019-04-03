FROM python:3.6
LABEL AUTHOR="Dominic Motuka <dominic.motuka@gmail.com>"
LABEL  app="njokeriosacco"

# prevent dpkg errors
ENV TERM=xterm-256color



ENV DJANGO_SETTINGS_MODULE=Espace.settings.base

WORKDIR  /app
COPY . /app/

# Set mirrors to Nearest Zone for faster builds
RUN sed -i "s/http:\/\/archive./http:\/\/nz.archive./g" /etc/apt/sources.list
RUN pip install -r requirements.txt


EXPOSE 8000

CMD  exec gunicorn Espace.wsgi:application --bind 0.0.0.0:8000 --workers 3