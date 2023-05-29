FROM ubuntu:latest
WORKDIR /app
RUN apt update
RUN apt install python3 python3-pip iputils-ping -y
COPY . .
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py", "--config", "/app/configs/conf.yaml"]
