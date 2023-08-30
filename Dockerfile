FROM python:3.11-slim

COPY . /app
WORKDIR /app

RUN python3 -m venv /opt/venv
RUN /opt/venv/bin/pip install -r requirements.txt

CMD [ "/opt/venv/bin/gunicorn", "-w", "2", "--bind", "0.0.0.0:5000", "app:app" ]
