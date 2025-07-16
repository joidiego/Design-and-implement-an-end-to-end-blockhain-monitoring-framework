FROM ubuntu:22.04

RUN apt update && apt install -y \
    build-essential \
    cmake \
    libzmq3-dev \
    libssl-dev \
    libsecp256k1-dev \
    git

WORKDIR /cpp-daemon
COPY cpp-daemon/ .

RUN mkdir build && cd build && cmake .. && make

CMD ["./daemon"]