FROM python:latest

WORKDIR .

COPY . .
RUN apt update

RUN apt install ffmpeg



RUN pip3 install -r requirements.txt

CMD ["start.sh"]

ENTRYPOINT ["bash"]
