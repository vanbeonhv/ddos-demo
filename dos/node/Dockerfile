FROM node:18-slim

WORKDIR /app
COPY server.js .

RUN apt update \
  && apt install -y htop \
  && apt clean

EXPOSE 3000
CMD ["node", "server.js"]
