# FROM python:3.10-buster
# WORKDIR /app
# RUN apk add --no-cache iputils build-base 
# COPY requirements.txt requirements.txt
# RUN pip3 install -r requirements.txt
# COPY . .
# CMD ["python3", "main.py", "--config", "/app/configs/conf.yaml"]



FROM ubuntu:latest
WORKDIR /app
RUN apt update
#RUN apt install python3 python3-pip iputils-ping -y
RUN apt install -y \
        python3 -y\
        python3-pip \
        iputils-ping \
        libcups2-dev\
        cups \
    && apt clean
COPY . .
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py", "--config", "/app/configs/conf.yaml"]
