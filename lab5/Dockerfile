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
    && rm -rf /var/lib/apt/lists/*
WORKDIR /home/jenkins
