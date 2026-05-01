FROM node:20-alpine AS deps

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

FROM node:20-alpine AS builder

WORKDIR /app

ARG APP_DOMAIN=robcotech.pro
ARG API_DOMAIN=api.robcotech.pro
ARG APP_URL=https://robcotech.pro
ARG API_URL=https://api.robcotech.pro
ARG GATEWAY_URL=https://api.robcotech.pro
ARG MEDIA_COMMERCE_URL=https://api.robcotech.pro

ENV APP_DOMAIN=$APP_DOMAIN
ENV API_DOMAIN=$API_DOMAIN
ENV APP_URL=$APP_URL
ENV API_URL=$API_URL
ENV GATEWAY_URL=$GATEWAY_URL
ENV MEDIA_COMMERCE_URL=$MEDIA_COMMERCE_URL
ENV NEXT_PUBLIC_API_URL=$API_URL
ENV NEXT_PUBLIC_APP_URL=$APP_URL
ENV NEXT_PUBLIC_GATEWAY_URL=$GATEWAY_URL

COPY --from=deps /app/node_modules ./node_modules
COPY . .

RUN npm run build

FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production
ENV PORT=3000
ENV HOSTNAME=0.0.0.0
ENV APP_DOMAIN=robcotech.pro
ENV API_DOMAIN=api.robcotech.pro
ENV APP_URL=https://robcotech.pro
ENV API_URL=https://api.robcotech.pro
ENV GATEWAY_URL=https://api.robcotech.pro
ENV MEDIA_COMMERCE_URL=https://api.robcotech.pro

COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
  CMD wget -q -O /dev/null http://localhost:3000/ || exit 1

CMD ["npm", "run", "start"]
