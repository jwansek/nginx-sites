#!/bin/sh

certbot certonly --manual --manual-auth-hook /app/acme-dns-auth.py --preferred-challenges dns --debug-challenges -d $1
