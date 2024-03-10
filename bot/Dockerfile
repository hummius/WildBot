FROM python:3.10-slim

WORKDIR /bot

COPY . .

RUN pip install -r requirements.txt

ENV PYTHONPATH /bot

ENTRYPOINT python main.py