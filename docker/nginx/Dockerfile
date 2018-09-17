FROM nginx:1.15.3-alpine

RUN mkdir -p /data/nginx

# openssl dhparam -out dhparam.pem 4096
COPY dhparam.pem /etc/nginx

COPY nginx.conf /etc/nginx/conf.d/default.conf
