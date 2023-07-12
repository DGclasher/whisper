FROM python:3.10.11

WORKDIR /app

COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

COPY . /app

CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "app:app" ]
