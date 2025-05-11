FROM node:18-alpine3.20

WORKDIR /app
RUN apk add --no-cache htop
COPY server.js .

CMD [ "node",  "server.js" ]