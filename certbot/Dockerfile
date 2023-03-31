FROM nginx
MAINTAINER Eden Attenborough "eddie.atten.ea29@gmail.com"
RUN apt-get update -y
RUN apt-get install -y cron python3-certbot-nginx wget
COPY . /app
WORKDIR /app

RUN wget https://github.com/joohoi/acme-dns-certbot-joohoi/raw/master/acme-dns-auth.py
RUN sed -i '1i #!/usr/bin/env python3' acme-dns-auth.py
RUN chmod +x acme-dns-auth.py

RUN echo "@monthly root certbot renew  --force-renewal > /proc/1/fd/1 2>/proc/1/fd/2" > /etc/crontab
ENTRYPOINT ["bash"]
CMD ["entrypoint.sh"]
