# syntax=docker/dockerfile:1.7

ARG PYTHON_IMAGE=python:3.11-slim-bookworm@sha256:917ec0e42cd6af87657a768449c2f604a6b67c7ab8e10ff917b8724799f816d3
ARG DEBIAN_IMAGE=debian:bookworm-slim@sha256:e899040a73d36e2b36fa33216943539d9957cba8172b858097c2cabcdb20a3e2
ARG DISTROLESS_IMAGE=gcr.io/distroless/python3-debian12@sha256:8ce6bba3f793ba7d834467dfe18983c42f9b223604970273e9e3a22b1891fc27

FROM ${PYTHON_IMAGE} AS wheels

WORKDIR /build

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_ROOT_USER_ACTION=ignore \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./
RUN python3 -m pip install --no-cache-dir --upgrade pip uv==0.6.12
RUN uv export \
      --format requirements-txt \
      --no-dev \
      --locked \
      --no-emit-project \
      --output-file requirements.lock

RUN --mount=type=cache,target=/root/.cache/pip,sharing=locked \
    python3 -m pip wheel --wheel-dir=/wheels --require-hashes -r requirements.lock

FROM ${PYTHON_IMAGE} AS python-deps

WORKDIR /build

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_ROOT_USER_ACTION=ignore \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY --from=wheels /wheels /wheels
COPY --from=wheels /build/requirements.lock /build/requirements.lock

RUN --mount=type=cache,target=/root/.cache/pip,sharing=locked \
    python3 -m pip install --upgrade pip && \
    python3 -m pip install \
      --require-hashes \
      --no-index --find-links=/wheels \
      --no-compile \
      --target=/opt/python \
      -r requirements.lock

FROM ${DEBIAN_IMAGE} AS runtime-deps

WORKDIR /tmp/debs

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    apt-get update && \
    apt-get download \
      bash \
      busybox-static \
      ca-certificates \
      libtinfo6 \
      libsqlite3-0 \
      libgcc-s1 \
      libstdc++6 && \
    mkdir -p /out && \
    for deb in ./*.deb; do dpkg-deb -x "$deb" /out; done && \
    rm -rf /var/lib/apt/lists/* /tmp/debs

FROM ${DISTROLESS_IMAGE} AS runtime

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    PYTHONPATH=/opt/python:/app \
    SQLITE_FILE_PATH=/data/book_api.db

COPY --from=runtime-deps /out/ /
COPY --from=python-deps /opt/python /opt/python
COPY --chown=65532:65532 book_api /app/book_api

USER 0:0

RUN ["python3", "-c", "import os, pathlib; pathlib.Path('/data').mkdir(parents=True, exist_ok=True); os.chown('/data', 65532, 65532); pathlib.Path('/bin/ls').exists() or os.symlink('/bin/busybox', '/bin/ls')"]

# distroless non-root user
USER 65532:65532

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD ["python3", "-c", "import json, urllib.request; r=urllib.request.urlopen('http://127.0.0.1:8000/healthcheck', timeout=2); data=json.load(r); assert data.get('status')=='ok'"]

ENTRYPOINT ["python3"]
CMD ["-m", "uvicorn", "book_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
