# Build stage from NodeJS Alpine
FROM node:10.16.0-alpine as build-stage

# Set Work directory
WORKDIR /app

# Copy packages
COPY package*.json ./

# Install packages
RUN npm install

# Copy installed packages
COPY . .

# Build distribution
RUN npm run build

# Production stage
FROM nginx:1.16.1-alpine as production-stage

# Copy file to NGINX http folder
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Export Port
EXPOSE 80

# RUN
CMD [ "nginx", "-g", "daemon off;"]