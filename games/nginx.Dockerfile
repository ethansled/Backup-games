FROM nginx
COPY pyproxy.conf /etc/nginx/conf.d/default.conf
EXPOSE 8080