FROM l4t:latest

# Definition of a Device & Service
ENV POSITION=Runtime \
    SERVICE=titaniadb-sentinel \
    AION_HOME=/var/lib/aion \
    MY_MYSQL_HOST=mysql \
    MY_MYSQL_USER=MYSQL_USER_XXX \
    MY_ETCD_HOST=titaniadb

RUN apt-get update && apt-get install -y libmysqlclient-dev

# Setup Directoties
RUN mkdir -p \
    $POSITION/$SERVICE
WORKDIR ${AION_HOME}/$POSITION/$SERVICE/

ADD requirements.txt .

RUN pip3 install -r requirements.txt

ADD src/ .

CMD ["python3", "-u", "main.py"]
