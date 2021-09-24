FROM python:3.9-alpine3.13
LABEL Author_Name="Oscar Hagman"
LABEL Author_Email="oscar.hagman@example.com"

RUN mkdir /app
WORKDIR /app
COPY . .
RUN apk add py3-pip
RUN pip3 install -r requirements.txt

CMD [ "python3", "app.py" ]

