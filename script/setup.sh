#!/bin/bash

function riscv_build_tools {
    sudo apt-get install make gcc-riscv64-unknown-elf -y
}

function python_env {
    sudo apt-get install python3 python3-venv python3-pip -y
}

function verilator_v5_044 {
    if command -v verilator >/dev/null 2>&1; then
        VERILATOR_REQUIRED_VERSION="5.044"
        VERILATOR_CURRENT_VERSION=$(verilator --version | awk '{print $2}')
        if [ "$VERILATOR_CURRENT_VERSION" == "$VERILATOR_REQUIRED_VERSION" ]; then
            return
        fi
    fi

    sudo apt install git -y

    # https://verilator.org/guide/latest/install.html#git-quick-install (last checked on: 25.02.26)
    
    # dependencies
    sudo apt-get install git help2man perl python3 make autoconf g++ flex bison ccache -y
    sudo apt-get install libgoogle-perftools-dev numactl perl-doc -y
    sudo apt-get install libfl2 -y
    sudo apt-get install libfl-dev -y
    sudo apt-get install zlibc zlib1g zlib1g-dev -y

    # source
    git clone https://github.com/verilator/verilator
    unset VERILATOR_ROOT
    cd verilator
    git pull
    git checkout v5.044

    # build
    autoconf
    ./configure
    make -j `nproc`
    sudo make install
    cd ..
    rm -rf verilator
}

function project_utils {
    sudo apt install patch tree cloc -y
}

########################################################################################################################
### MAIN
########################################################################################################################
sudo apt update

riscv_build_tools
python_env
verilator_v5_044
project_utils
