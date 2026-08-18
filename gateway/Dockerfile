# Standalone Dockerfile for Edge Gateway
FROM node:26-alpine AS builder

WORKDIR /app

COPY package.json yarn.lock* ./
RUN yarn install

COPY tsconfig.json ./
COPY src ./src
RUN yarn build

# Stage de Produção
FROM node:26-alpine AS runner

WORKDIR /app
ENV NODE_ENV=production

COPY package.json yarn.lock* ./
RUN yarn install --production

COPY --from=builder /app/dist ./dist

EXPOSE 8080

CMD ["node", "dist/server.js"]
