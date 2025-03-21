FROM telegraf:1.34.0

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends openssh-client sudo

RUN echo "telegraf ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers