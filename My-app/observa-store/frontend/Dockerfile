# frontend/Dockerfile
 
# Stage 1: Build the React application
FROM node:18-alpine AS build
 
# Set the working directory inside the container
WORKDIR /app
 
# Copy package.json and package-lock.json to leverage Docker's caching mechanism
COPY package*.json ./
 
# Install project dependencies
RUN npm install
 
# Copy the rest of the application's source code, including the 'public' and 'src' folders
COPY . .
 
# Build the application for production
# The build script will now be able to find /app/public/index.html
RUN npm run build
 
# Stage 2: Set up the production environment with Nginx
FROM nginx:1.21-alpine
 
# Copy the built application from the 'build' stage to Nginx's web server directory
COPY --from=build /app/build /usr/share/nginx/html
 
# Expose port 80 to allow traffic to the web server
EXPOSE 80
 
# Start Nginx in the foreground when the container launches
CMD ["nginx", "-g", "daemon off;"]
