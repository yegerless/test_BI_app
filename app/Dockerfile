FROM python:3.12.2

USER root

WORKDIR /usr/src/app

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8050", "Dashboard.wsgi:application"]
