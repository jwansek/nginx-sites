# nginx sites

This is how all of my websites communicate to the outside world: a collection of nginx configs and SSH tunnels.

[eda.gay](https://eda.gay), [git.eda.gay](https://git.eda.gay), [jellyfin.eda.gay](https://jellyfin.eda.gay) and [nc.eda.gay](https://nc.eda.gay) all are served directly from my home server with the nginx configs in this repo. [nitter.eda.gay](https://nitter.eda.gay), [invidious.eda.gay](https://invidious.eda.gay) and [bibliogram.eda.gay](https://bibliogram.eda.gay) are all hosted on this server, but are proxied to a VPS. This is done using a [reverse SSH tunnel](https://github.com/jwansek/ReverseSSHTunnel)

## HTTPS with letsencrypt

`certbot` is the container managing HTTPS keys. It renews keys monthly using a cronjob. It is also used to setup HTTPS in the first place. Unfortunately I have only managed to get DNS validation to work, which isn't the default for certbot. 

`sudo docker exec -it nginx-sites_certbot_1 ./dns_certonly.sh eda.gay`

Can be used to interactively setup HTTPS for the site `eda.gay`. It involves setting a given CNAME record in the DNS provider to tell certbot who we are. This is repeated for all the subdomains. Then the certificates can be setup:

`sudo docker exec -it nginx-sites_certbot_1 certbot install --nginx`

## TODOs

- [ ] add logging in a container by using [autoLogger](https://github.com/jwansek/autoLogger)
