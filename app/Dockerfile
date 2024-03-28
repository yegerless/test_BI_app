FROM python:3.12.2

USER root

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

#CMD ["gunicorn", "-b", "0.0.0.0:8050", "Dashboard.wsgi:application"]

EXPOSE 5000
