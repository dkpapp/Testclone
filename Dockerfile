FROM python:latest

WORKDIR .

COPY . .

RUN pip3 install -r requirements.txt

CMD ["start.sh"]

ENTRYPOINT ["bash"]
