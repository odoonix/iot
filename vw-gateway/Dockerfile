FROM ubuntu:latest
WORKDIR /app
RUN apt update
RUN apt install python3 python3-pip iputils-ping -y
#RUN apt-get update -y \
#    && apt-get install -y \
#        python3.10 \
#        python-pip \
#        iputils-ping \
#        pip3 install cryptography --break-system-packages\
#    && apt-get clean
COPY . .
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py", "--config", "/app/configs/conf.yaml"]
