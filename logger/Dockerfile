FROM debian:11.5-slim
MAINTAINER Eden Attenborough "eda@e.email"
ENV TZ=Europe/London
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev cron
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

RUN echo "*/2 * * * * root python3 /app/autoLogger.py > /proc/1/fd/1 2>/proc/1/fd/2" > /etc/crontab
RUN echo "@hourly root python3 /app/export.py > /proc/1/fd/1 2>/proc/1/fd/2" >> /etc/crontab

ENTRYPOINT ["bash"]
CMD ["entrypoint.sh"]
