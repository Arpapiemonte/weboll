ARG FRONTEND_BASE_IMAGE=deps-frontend-base

FROM node:16 AS deps-frontend-base
# Requirements are installed here to ensure they will be cached.
WORKDIR /app
COPY ./package.json ./yarn.lock ./
RUN yarn

FROM ${FRONTEND_BASE_IMAGE} AS frontend-builder
WORKDIR /app
COPY .eslintrc.cjs .gitignore index.html vite.config.js vitest.config.js ./
COPY config/copyright.js ./config/copyright.js
COPY public ./public
COPY src ./src
COPY w05 ./w05
COPY w16 ./w16
COPY w23 ./w23
COPY w24 ./w24
COPY w29 ./w29
COPY w22 ./w22
COPY w30 ./w30
COPY w22verifica ./w22verifica
COPY w31 ./w31
COPY .env ./.env
COPY w32 ./w32
RUN yarn build

FROM nginx AS frontend
COPY --from=frontend-builder /app/dist /usr/share/nginx/html
