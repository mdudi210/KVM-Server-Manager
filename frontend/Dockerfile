FROM node:20.15.1

WORKDIR /app

# Copy package files first for better caching
COPY frontend/package*.json frontend/jsconfig.json ./

RUN npm install

# Copy the frontend directory
COPY frontend/ .

EXPOSE 8080

CMD ["npm", "run", "serve", "--", "--host", "0.0.0.0"]