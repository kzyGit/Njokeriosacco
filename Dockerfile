FROM python:3 

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/
EXPOSE 8000
RUN pip install -r requirements.txt 
CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000