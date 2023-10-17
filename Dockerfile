FROM python:3.11.6-alpine3.18

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY checker.py ./

ENV TOKEN=
ENV CHAT_ID=
ENV DATA_FILE=

CMD [ "python", "/app/checker.py"]
