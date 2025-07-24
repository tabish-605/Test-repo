
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
RUN npm install --save-dev typescript @types/node @types/react
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app .
ENV PORT 3000
CMD ["npm", "start"]
