FROM node:22-slim AS base

WORKDIR /usr/app

COPY ./package*.json ./

RUN npm install

#FROM llm-chatbot-api-image-base:latest
FROM base AS final

ARG API_PORT

COPY . .

RUN npm run build

USER node

EXPOSE ${API_PORT}

CMD ["npm", "start"]