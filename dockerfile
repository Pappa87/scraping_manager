FROM python:3
COPY . /app/
RUN pip install -r /app/requirements.txt
WORKDIR /app
RUN mv docker_config.py config.py

