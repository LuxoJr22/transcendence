FROM node:lts-alpine AS build-stage

WORKDIR /app
COPY . .
RUN npm install
RUN apk update && apk upgrade && apk search curl && apk add curl
RUN npm run build

FROM nginx:stable-alpine AS production-stage

COPY --from=build-stage /app/build /var/www/html
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

RUN apk add openssl
RUN mkdir -p /etc/nginx/certification
RUN openssl genpkey -algorithm RSA -out /etc/nginx/certification/key.pem
RUN openssl req -new -x509 -key /etc/nginx/certification/key.pem -out /etc/nginx/certification/cert.pem -days 365 -subj "/C=FR/ST=PACA/L=Nice/O=42nice/OU=42nice/CN=mpelazza"

RUN chown -R nginx:nginx /var/www/html

ENTRYPOINT [ "nginx", "-g", "daemon off;" ]