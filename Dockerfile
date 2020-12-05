FROM ubuntu:20.04

RUN apt-get update -y
RUN apt-get install -y git python3 python3-dev gcc libmysqlclient-dev mysql-server mysql-client virtualenv wget
RUN apt-get update -y
RUN apt-get install -y apt-utils mysql-server
RUN apt-get install --fix-missing
RUN apt-get install -y libmysqlclient-dev sudo

RUN apt-get update -y
RUN apt-get install -y python3-pip wget nano

RUN mkdir -p /var/syllabify
WORKDIR /var/syllabify
COPY . .

RUN pip3 install -r /var/syllabify/requirements.txt

CMD ["/bin/bash","-c","chmod +x /var/syllabify/startup.sh && /var/syllabify/startup.sh"]