FROM python:2.7

MAINTAINER Sam Ho <samhocngz@gmail.com>

RUN pip install virtualenv

RUN mkdir -p /data/mymedia
RUN mkdir -p /data/upload

RUN virtualenv /data/venv

COPY . /data/mymedia/

RUN pip install -r /data/mymedia/requirements.txt

WORKDIR /data/mymedia

VOLUME ["/data/upload"]

EXPOSE 5000

CMD ["python", "manage.py", "runserver", "-h", "0.0.0.0"]