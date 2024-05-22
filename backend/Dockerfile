FROM python:3.10-alpine

RUN mkdir app

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY start.sh .

RUN chmod +x start.sh

ENTRYPOINT ["sh", "./start.sh"]