FROM node:20.15.1

WORKDIR /app

COPY package*.json jsconfig.json ./

RUN npm install

COPY . .

EXPOSE 8080

CMD ["npm", "run", "serve"]