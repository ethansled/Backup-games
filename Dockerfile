FROM python:3 AS builder
RUN apt update && apt install ffmpeg -y
RUN pip install pygbag
WORKDIR /usr/src/app
COPY games ./
COPY build.sh .
RUN bash build.sh

FROM nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
RUN rm -rf /usr/share/nginx/html && mkdir /usr/share/nginx/html
COPY --from=builder /usr/src/app/html /usr/share/nginx/html
EXPOSE 8080