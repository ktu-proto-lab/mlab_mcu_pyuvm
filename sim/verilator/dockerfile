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

# files created inside the container can be also edited outside of it
ARG USERNAME=user
ARG USER_UID=1000
ARG USER_GID=1000

RUN touch /var/mail/ubuntu && chown ubuntu /var/mail/ubuntu \
    && userdel -r ubuntu || true \
    && groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt update \
    && apt install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

RUN mkdir -p /home/mcu/uvm && chown -R $USERNAME:$USERNAME /home/mcu

USER $USERNAME

WORKDIR /home/mcu/uvm

CMD ["/bin/bash"]
