FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN apt-get update && \ apt-get install -y erlang rabbitmq-server libpq-dev python3-dev ffmpeg
RUN systemctl enable rabbitmq-server
RUN systemctl start rabbitmq-server
COPY . /code/
