FROM ubuntu:22.04

WORKDIR /usr/app
COPY . .

ENV ACCEPT_EULA=Y

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y software-properties-common build-essential libopenblas-dev ninja-build pkg-config cmake-data clang \
    git curl wget zip unzip \
    python3 python3-pip python-is-python3

RUN python3 -m pip install --upgrade pip

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
RUN rustup target add wasm32-wasi

# Install WasmEdge with an LLM inference backend
RUN curl -sSf https://raw.githubusercontent.com/WasmEdge/WasmEdge/master/utils/install_v2.sh | bash
ENV PATH="/root/.wasmedge/bin:${PATH}"
RUN curl -LO https://github.com/LlamaEdge/LlamaEdge/releases/latest/download/llama-simple.wasm

CMD ["python3", "main.py"]