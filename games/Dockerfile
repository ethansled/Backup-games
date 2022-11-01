FROM python:3.10

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt install ffmpeg

COPY . .
ENTRYPOINT [ "/usr/local/bin/python", "-m", "pygbag", "--port", "8080"]
CMD [ "--hostname number-guesser", "number-guesser" ]