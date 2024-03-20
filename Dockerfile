FROM python:3.12.2

USER root

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./Dashboard/Dashboard.py"]
