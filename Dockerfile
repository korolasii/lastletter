FROM python:3.9

RUN mkdir -p /docker/app/lastletter/
WORKDIR /docker/app/lastletter/

COPY . /docker/app/lastletter/
RUN pip install -r req.txt

CMD ["python","main.py"]
