FROM node:lts-alpine

WORKDIR /app
COPY . .
RUN npm install
RUN apk update && apk upgrade && apk search curl && apk add curl

CMD npm run dev -- --host
