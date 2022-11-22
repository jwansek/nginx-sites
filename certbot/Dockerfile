FROM nginx
MAINTAINER Eden Attenborough "eddie.atten.ea29@gmail.com"
RUN apt-get update -y
RUN apt-get install -y cron python3-certbot-nginx
COPY . /app
WORKDIR /app

RUN echo "@monthly root certbot renew > /proc/1/fd/1 2>/proc/1/fd/2" > /etc/crontab
ENTRYPOINT ["bash"]
CMD ["entrypoint.sh"]
