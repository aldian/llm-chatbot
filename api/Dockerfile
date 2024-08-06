FROM llm-chatbot-api-image-base:latest

ARG API_PORT

COPY . .

RUN npm run build

USER node

EXPOSE ${API_PORT}

CMD ["npm", "start"]