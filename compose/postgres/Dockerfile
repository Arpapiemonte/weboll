FROM postgres:13 AS curl

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    curl \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*
