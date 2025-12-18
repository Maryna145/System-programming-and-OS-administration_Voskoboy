FROM jenkins/ssh-agent:jdk17

USER root

RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    rpm \
    dpkg-dev \
    fakeroot \
    curl \
    wget \
    docker.io \
    sudo \
    && rm -rf /var/lib/apt/lists/*
RUN echo "jenkins ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
WORKDIR /home/jenkins
