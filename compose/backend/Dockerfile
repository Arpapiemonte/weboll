ARG TEST_BASE_IMAGE=deps-backend-base
ARG APP_BASE_IMAGE=deps-test

FROM debian:bookworm-slim AS deps-backend-base

ARG LDAP_CA=./compose/ldap/certs/ca.crt
ARG LOCAL_CA=./compose/ldap/certs/ca.crt
ARG DOMAIN="example.com"
COPY "$LDAP_CA" /usr/local/share/ca-certificates/ca1.crt
COPY "$LOCAL_CA" /usr/local/share/ca-certificates/ca2.crt
COPY ./compose/fonts/Titillium_Web.zip /tmp

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    fontconfig \
    fonts-liberation \
    lftp \
    imagemagick \
    ghostscript \
    locales \
    openssh-client \
    ldap-utils \
    wkhtmltopdf \
    procps \
    sshpass \
    tcpdump \
    unzip \
    wait-for-it \
    wget \
    postfix \
    python3-pip \
    libpq-dev \
    build-essential \
    python3-dev \
    libldap2-dev \
    libsasl2-dev \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/* \
  && unzip -d /usr/local/share/fonts/ /tmp/Titillium_Web.zip \
  && fc-cache \
  && sed -i -e 's/# it_IT.UTF-8 UTF-8/it_IT.UTF-8 UTF-8/' /etc/locale.gen \
  && dpkg-reconfigure --frontend=noninteractive locales \
  && chmod 644 /usr/local/share/ca-certificates/ca1.crt \
  && chmod 644 /usr/local/share/ca-certificates/ca2.crt \
  && apt-get -y remove fonts-dejavu-core

# This package change allerta and vigilanza header
RUN sed -i '/policy domain="coder" rights="none" pattern="PDF"/d' /etc/ImageMagick-6/policy.xml

# Configure postfix
RUN sed -i "/^#myorigin.*/a myorigin = weboll.${DOMAIN}" /etc/postfix/main.cf \
  && sed -i "s/^relayhost =.*/relayhost = [smtp.${DOMAIN}]/" /etc/postfix/main.cf \
  && sed -i "\$amaillog_file = /var/log/maillog" /etc/postfix/main.cf \
  && echo "weboll.${DOMAIN}" > /etc/mailname

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip3 install --break-system-packages --no-cache-dir -r /requirements/app.txt

COPY ./compose/backend/ldap.conf /etc/ldap/ldap.conf

FROM ${TEST_BASE_IMAGE} AS deps-test

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    black \
    chromium-driver \
    flake8 \
    gettext \
    git \
    imagemagick \
    isort \
    mypy \
    postgresql-client \
    pre-commit \
    sqlite3 \
    strip-nondeterminism \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/* \
  && pip3 install --break-system-packages --no-cache-dir -r /requirements/test.txt

# This package change allerta and vigilanza header
RUN sed -i '/policy domain="coder" rights="none" pattern="PDF"/d' /etc/ImageMagick-6/policy.xml

FROM ${APP_BASE_IMAGE} AS backend

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

COPY . /app

WORKDIR /app
