FROM python:3.10

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt update -y
RUN apt install ffmpeg -y

COPY . .
EXPOSE 8080