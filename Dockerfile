FROM alpine

RUN apk upgrade && apk add python3 && pip3 install -U pip

WORKDIR /usr

RUN mkdir flaskserver

WORKDIR /usr/flaskserver

COPY . .

RUN pip3 install -r requirements.txt

ENV FLASK_APP PythonServer.py

#ENV FLASK_DEBUG 1

EXPOSE 5000

CMD ["python3", "-m", "flask","run", "-h", "0.0.0.0"]