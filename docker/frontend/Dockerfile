# ==============================================================================
# OIL Safety Intelligence Platform — Frontend Dockerfile
# Multi-Stage Build: Node 20 Build -> Nginx Alpine Production
# ==============================================================================

FROM node:20-alpine as builder

WORKDIR /app

COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci || npm install

COPY frontend/ .
RUN npm run build

# --- Runtime Stage ---
FROM nginx:1.25-alpine as runner

COPY docker/frontend/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
