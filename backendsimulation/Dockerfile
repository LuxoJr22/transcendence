FROM node:lts-alpine

WORKDIR /app
COPY . .
RUN npm install -g json-server

CMD json-server --watch db.json