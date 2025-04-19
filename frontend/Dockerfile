# Build stage - This stage is only used to build the application
FROM node:20-alpine AS builder

# Set working directory
WORKDIR /app

# Clean npm cache and remove existing files
RUN npm cache clean --force && \
    rm -rf node_modules package-lock.json

# Copy package files first to leverage Docker cache
COPY package*.json ./

# Install dependencies fresh with legacy peer deps
RUN npm install --legacy-peer-deps

# Install specific versions of build tools
RUN npm install vite@5.1.0 @vitejs/plugin-react@4.2.1 esbuild@0.25.2

# Copy the rest of the application code
COPY . .

# Rebuild esbuild to ensure correct version
RUN npm rebuild esbuild

# Build the application
# This creates optimized production build in /app/dist
RUN npm run build

# Production stage - This is the final image that will be deployed
FROM nginx:alpine

# Remove default nginx static assets
RUN rm -rf /usr/share/nginx/html/*

# Copy built files from builder stage to nginx directory
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 for HTTP traffic
EXPOSE 80

# Start nginx in foreground
CMD ["nginx", "-g", "daemon off;"] 