ARG FRONTEND_BASE_IMAGE=deps-frontend-base

FROM node:22 AS deps-frontend-base
# Requirements are installed here to ensure they will be cached.
WORKDIR /app
COPY ./package.json ./yarn.lock ./
RUN yarn

FROM ${FRONTEND_BASE_IMAGE} AS frontend-builder
WORKDIR /app
COPY .eslintrc.cjs .gitignore index.html vite.config.ts vitest.config.ts ./
COPY config/copyright.js ./config/copyright.js
COPY public ./public
COPY src ./src
COPY w05 ./w05
COPY w06 ./w06
COPY w07 ./w07
COPY w12 ./w12
COPY w15 ./w15
COPY w16 ./w16
COPY w17 ./w17
COPY w20 ./w20
COPY w21 ./w21
COPY w23 ./w23
COPY w24 ./w24
COPY w26 ./w26
COPY w28 ./w28
COPY w29 ./w29
COPY w22 ./w22
COPY w30 ./w30
COPY w22verifica ./w22verifica
COPY w17verifica ./w17verifica
COPY w31 ./w31
COPY w32 ./w32
COPY w33 ./w33
COPY w34 ./w34
COPY w35 ./w35
COPY w37 ./w37
COPY w36 ./w36
COPY w99 ./w99
COPY .env ./.env
RUN yarn build

FROM nginx AS frontend
COPY --from=frontend-builder /app/dist /usr/share/nginx/html
