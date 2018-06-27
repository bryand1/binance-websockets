FROM python:3.6.5

WORKDIR /usr/src
COPY ./src .

CMD ["python", "main.py"]
