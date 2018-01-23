FROM python:2.7.14-jessie


RUN mkdir /app
WORKDIR /app


COPY tools/requirements.txt ./

RUN pip install --require-hashes -r requirements.txt
COPY . .
RUN  pip install .


ENTRYPOINT ["garecovery-cli", "2of2scan", "-o garecovery.csv", "--destination-address"]
