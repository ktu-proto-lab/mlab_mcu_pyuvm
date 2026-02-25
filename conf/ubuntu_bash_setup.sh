sudo apt update

# installation for compiling c code
sudo apt-get install make gcc-riscv64-unknown-elf -y

# running cocotb environment
sudo apt-get install python3 python3-venv python3-pip -y

# verilator
# source: https://verilator.org/guide/latest/install.html#git-quick-install (last checked on: 25.02.26)

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
