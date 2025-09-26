################################################################################
# Build
#
FROM node:lts-alpine AS builder

WORKDIR /src

COPY . /src
RUN npm install
RUN npm run build


################################################################################
# Prod
#
FROM python:3.13-alpine

# -------------------------------------------- Set environment and ARG variables
ENV \
    # Set default PUID / PGUID \
    PUID=1000 \
    PGID=1000 \
    # Setup s6 overlay
    S6_CMD_WAIT_FOR_SERVICES_MAXTIME=0 \
    S6_VERBOSITY=1
ARG \
    # Set version for s6 overlay \
    ARG S6_OVERLAY_VERSION="3.2.1.0" \
    ARG S6_OVERLAY_ARCH="x86_64"

# ------------------------------------------------------------------- s6 overlay
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-${S6_OVERLAY_ARCH}.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-${S6_OVERLAY_ARCH}.tar.xz
# Optional symlinks
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-${S6_OVERLAY_ARCH}.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-${S6_OVERLAY_ARCH}.tar.xz

# ------------------------------------------------------------ SeedboxSync setup
RUN apk add --update --no-cache shadow
RUN addgroup -g ${PGID} seedboxsync && adduser -D -u ${PUID} -G seedboxsync seedboxsync

# System folders
RUN mkdir /config && \
    mkdir /downloads && \
    mkdir /watch && \
    mkdir /app && \
    chown -R seedboxsync:seedboxsync /config /downloads /watch

# Install app
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -e . && \
    pip install --no-cache-dir gunicorn && \
    rm -rf /app/docker /app/*.json /app/*.js
COPY --from=builder /src/seedboxsync_front/static/dist /app/seedboxsync_front/static

# Seedboxsync folders
RUN chown -R seedboxsync:seedboxsync /app && \
    mkdir /home/seedboxsync/.config && \
    ln -s /config /home/seedboxsync/.config/seedboxsync && \
    ln -s /downloads /home/seedboxsync/Downloads && \
    ln -s /watch /home/seedboxsync/watch

# Copy all rootfs files with configuration and others scripts
COPY docker/ /
RUN chmod 755 /etc/s6-overlay/s6-rc.d/*/run && \
    chmod 755 /etc/s6-overlay/s6-rc.d/*/up

# healthcheck
HEALTHCHECK --interval=1m --start-period=1m CMD wget --no-verbose --tries=1 http://localhost:8000/ -q -O /dev/null || exit 1

WORKDIR /app
EXPOSE 8000

ENTRYPOINT ["/init"]
