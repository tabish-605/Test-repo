# frontend/Dockerfile
 
# Stage 1: Build the React application
FROM node:18-alpine AS build
 
WORKDIR /app
 
COPY package*.json ./
 
RUN npm install
 
# Copy the rest of the application's source code
COPY . .
 
# --- START DEBUGGING ---
# The following lines will print the file structure inside the container.
# This helps verify that your files, especially public/index.html, are copied correctly.
RUN echo "--- Listing contents of /app directory: ---" && ls -la /app
RUN echo "--- Listing contents of /app/public directory: ---" && ls -la /app/public
# --- END DEBUGGING ---
 
# Build the application for production
RUN npm run build
 
# Stage 2: Set up the production environment with Nginx
FROM nginx:1.21-alpine
 
# Copy the built application from the 'build' stage to Nginx's web server directory
COPY --from=build /app/build /usr/share/nginx/html
 
# Expose port 80 to allow traffic to the web server
EXPOSE 80
 
# Start Nginx in the foreground when the container launches
CMD ["nginx", "-g", "daemon off;"]
