FROM ubuntu:22.04

# Instal dependensi — PENTING: tambahkan libssl-dev
RUN apt update && apt install -y \
    build-essential \
    cmake \
    libzmq3-dev \
    pkg-config \
    git \
    autoconf \
    automake \
    libtool \
    libssl-dev  # ← Ini yang hilang!

WORKDIR /tmp

# Clone dan compile libsecp256k1
RUN git clone https://github.com/bitcoin-core/secp256k1.git && \
    cd secp256k1 && \
    ./autogen.sh && \
    ./configure --enable-module-recovery --enable-experimental --prefix=/usr/local && \
    make && \
    make install && \
    ldconfig

# Tambahkan /usr/local/lib/pkgconfig ke pencarian pkg-config
RUN mkdir -p /etc/pkgconfig/path.d && \
    echo "/usr/local/lib/pkgconfig" > /etc/pkgconfig/path.d/secp256k1.conf

WORKDIR /cpp-daemon
COPY cpp-daemon/ .

# Debug: Pastikan file .pc ada dan pkg-config bisa melihatnya
RUN echo "🔍 Isi /usr/local/lib/pkgconfig:"
RUN ls -la /usr/local/lib/pkgconfig/
RUN echo "🔍 Isi file libsecp256k1.pc:"
RUN cat /usr/local/lib/pkgconfig/libsecp256k1.pc
RUN pkg-config --exists libsecp256k1 && echo "✅ BERHASIL: libsecp256k1 ditemukan!" || (echo "❌ GAGAL" && exit 1)

# Build C++ daemon
RUN mkdir build && cd build && cmake .. && make

CMD ["./build/daemon"]