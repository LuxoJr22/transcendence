FROM node:lts-alpine

WORKDIR /app
COPY . .
RUN npm install -g json-server

EXPOSE 8000

CMD json-server --watch db.json --port 8000