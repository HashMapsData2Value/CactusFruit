# syntax=docker/dockerfile:1

FROM python:3.10

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 5000

COPY src/app.py app.py
COPY src/utils.py utils.py

ARG ALGORAND_API
ENV ALGORAND_API $ALGORAND_API

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]