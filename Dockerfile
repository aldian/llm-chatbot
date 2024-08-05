# Use the official Ubuntu 22.04 as the base image
FROM ubuntu:22.04

WORKDIR /usr/app
COPY . .

# Set the environment variable to accept the EULA
ENV ACCEPT_EULA=Y

# Update and upgrade the system
RUN apt-get update && apt-get upgrade -y

# Install necessary packages
RUN apt-get install -y software-properties-common build-essential libopenblas-dev ninja-build pkg-config cmake-data clang \
    git git-lfs curl wget zip unzip \
    python3 python3-pip python-is-python3

# Install Git LFS
RUN git lfs install

# Upgrade pip and install required Python packages
RUN python3 -m pip install --upgrade pip \
    && pip install pytest cmake scikit-build setuptools fastapi uvicorn sse-starlette pydantic-settings sentencepiece numpy==1.26.4 \
    && pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu \
    && pip install sentencepiece pyyaml

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
RUN rustup target add wasm32-wasi

# Install WasmEdge with an LLM inference backend
RUN curl -sSf https://raw.githubusercontent.com/WasmEdge/WasmEdge/master/utils/install_v2.sh | bash
ENV PATH="/root/.wasmedge/bin:${PATH}"

RUN curl -LO https://github.com/LlamaEdge/LlamaEdge/releases/latest/download/llama-simple.wasm
RUN curl -LO https://github.com/second-state/LlamaEdge/releases/latest/download/llama-chat.wasm
RUN curl -LO https://github.com/LlamaEdge/LlamaEdge/releases/latest/download/llama-api-server.wasm

# Start the script
CMD ["python3", "main.py"]
