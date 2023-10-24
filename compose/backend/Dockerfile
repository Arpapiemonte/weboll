ARG TEST_BASE_IMAGE=deps-backend-base
ARG APP_BASE_IMAGE=deps-test

FROM debian:bookworm-slim AS deps-backend-base

ENV TITILLIUM /tmp/titillium
ARG LDAP_CA=./compose/ldap/certs/ca.crt
ARG LOCAL_CA=./compose/ldap/certs/ca.crt
COPY "$LDAP_CA" /usr/local/share/ca-certificates/ca1.crt
COPY "$LOCAL_CA" /usr/local/share/ca-certificates/ca2.crt

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    fontconfig \
    lftp \
    graphicsmagick-imagemagick-compat \
    ghostscript \
    locales \
    openssh-client \
    python3-argon2 \
    python3-cryptography \
    python3-distlib \
    python3-ldap \
    ldap-utils \
    python3-factory-boy \
    python3-hiredis \
    python3-pil \
    python3-pip \
    python3-psycopg2 \
    python3-rcssmin \
    python3-redis \
    python3-requests \
    python3-slugify \
    python3-tz \
    python3-wheel \
    python3-whitenoise \
    python3-yaml \
    wkhtmltopdf \
    procps \
    sshpass \
    tcpdump \
    unzip \
    wait-for-it \
    wget \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/* \
  && mkdir -p "$TITILLIUM" \
  && wget -q -O "$TITILLIUM/Titillium_Web.zip" https://fonts.google.com/download?family=Titillium%20Web \
  && unzip -d /usr/local/share/fonts/ "$TITILLIUM/Titillium_Web.zip" \
  && rm -rf "$TITILLIUM" \
  && fc-cache \
  && sed -i -e 's/# it_IT.UTF-8 UTF-8/it_IT.UTF-8 UTF-8/' /etc/locale.gen \
  && dpkg-reconfigure --frontend=noninteractive locales \
  && chmod 644 /usr/local/share/ca-certificates/ca1.crt \
  && chmod 644 /usr/local/share/ca-certificates/ca2.crt \
  && apt-get -y remove fonts-dejavu-core

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
    python3-coverage \
    python3-flake8 \
    python3-ipdb \
    python3-pylint-django \
    python3-pytest \
    python3-pytest-django \
    python3-pytest-sugar \
    sqlite3 \
    strip-nondeterminism \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/* \
  && pip3 install  --break-system-packages --no-cache-dir -r /requirements/test.txt

# This package change allerta and vigilanza header
RUN sed -i '/policy domain="coder" rights="none" pattern="PDF"/d' /etc/ImageMagick-6/policy.xml

FROM ${APP_BASE_IMAGE} AS backend

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY . /app

WORKDIR /app
