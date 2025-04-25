# base image (Ubuntu 22.04)
FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

# 1) install basic tools
RUN apt-get update && \
    apt-get install -y \
      curl git make build-essential \
      python3.11 python3.11-venv python3-pip \
      docker.io kubectl helm \
    && rm -rf /var/lib/apt/lists/*

# 2) Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH=/root/.cargo/bin:${PATH}
RUN rustup default 1.81.0

# 3) setting alias to use uv
RUN ln -s /usr/bin/pip3 /usr/local/bin/uv

# 4) project working directory
WORKDIR /workspace

# 5) create & activate Python venv
RUN python3.11 -m venv /opt/venv
ENV PATH=/opt/venv/bin:${PATH}

# 6) copy code & install dependencies
COPY requirements.txt /workspace/
RUN uv install --upgrade pip && \
    uv install -r requirements.txt

# 7) activate venv automatically when starting basic shell
RUN echo "source /opt/venv/bin/activate" >> /etc/bash.bashrc
