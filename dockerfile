FROM ubuntu:24.04@sha256:d1e2e92c075e5ca139d51a140fff46f84315c0fdce203eab2807c7e495eff4f9

ENV DEBIAN_FRONTEND=noninteractive

# Dependencies
# tools:                            git, make
# riscv build tools:                gcc-riscv64-unknown-elf
# python environment:               python3, python3-venv, python3-pip
# verilator build  dependencies:    help2man, perl, autoconf, g++, flex, bison, ccache, libgoogle-perftools-dev,
#                                   numactl, perl-doc, libfl2, libfl-dev, zlib1g, zlib1g-dev
# gtkwave and gui:                  gtkwave, x11-utils
# project utils:                    patch, cloc, tree
RUN apt update && \
    apt install -y --no-install-recommends \
        git make \
        gcc-riscv64-unknown-elf \
        python3 python3-dev python3-venv python3-pip \
        help2man perl autoconf g++ flex bison ccache \
        libgoogle-perftools-dev numactl perl-doc \
        libfl2 libfl-dev zlib1g zlib1g-dev \
        gtkwave x11-utils \
        patch cloc tree && \
    rm -rf /var/lib/apt/lists/*

# verilator v5.044
WORKDIR /tmp/verilator
RUN git clone https://github.com/verilator/verilator && \
    cd verilator && \
    git checkout v5.044 && \
    autoconf && \
    ./configure && \
    make -j $(nproc) && \
    make install && \
    rm -rf /tmp/verilator

WORKDIR /home/mcu/uvm

CMD ["/bin/bash"]
