# Stage 1: build
FROM node:20-alpine as build
WORKDIR /app
COPY package.json ./
RUN npm install --legacy-peer-deps
COPY . .
RUN npm run build

# Stage 2: serve
FROM nginx:1.25-alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx","-g","daemon off;"]