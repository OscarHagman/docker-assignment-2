FROM python:3.9-alpine
LABEL Maintainer="Oscar Hagman"

WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .

CMD [ "python", "app.py" ]
