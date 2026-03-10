# IBEX RISC-V Microcontroller UVM Testing Framework

## Cloning the Project

### Project

#### Initial Setup

```bash
# Clone the root project
git clone --recurse-submodules https://github.com/dovydasliutkus/MLAB_MCU_edu.git
# Enter 'uvm' project
cd MLAB_MCU_edu/uvm
# The submodule can be in the unatached HEAD state, checkout to main
git checkout main
```

`main` branch is the stable one and `dev` can have unstable or broken code

#### Updating

```bash
# Inside root project 'MLAB_MCU_edu'
git pull
git submodule update --init --recursive
# Enter 'uvm' submodule
cd uvm
# The submodule can be in the unatached HEAD state, checkout to main
git checkout main
# Pull latest changes
git pull
```
## Initializing Working Environment
### Ubuntu
To run on Ubuntu or Ubuntu-based Linux operating systems, use `setup.sh` script for automatic tool instalation:
```bash
./script/setup.sh
```
### Docker
If you are on other platforms that are not Ubuntu or Debian based, download [Docker](https://www.docker.com/).

Run the `init.sh` script with `--docker` flag, note that docker requires `sudo` access.

```bash
./script/init.sh --docker
```

On the first setup you may need to add yourself to the docker group, after this setup, just run `newgrp docker` and rerun the script.

```
$ ./script/init.sh --docker
[WARNING]: docker requires sudo or user lacks permissions
[INFO   ]: adding user 'la_52' to docker group...
[sudo] password for la_52: 
[INFO   ]: please log out and log back in, reboot, or run: 'newgrp docker'
$ newgrp docker
$ ./script/init.sh --docker
```

Running the second time script will build docker image and run it's container:

```
[INFO   ]: building docker image
...
[INFO   ]: running docker container
...
[SUCCESS]: you are now inside built container
```

You are inside docker container:
```
root@mlab:/home/mcu/uvm# 
```
Use to run simulations, compile code, generate reports. Local files are linked with the container, edit files from your local machine, do not edit them inside the docker, that is general tip.

### Python's Virtual Environment

When the setup is completed, run second project initialization step (run script inside the Docker container if you are using it):

```bash
./script/init.sh --env
```

### Optional: Run Sanity Test

It runs GPIO Mirror test (as of 09.03.26):
```
./script/init.sh --test
```

Expected output:
```
10015090.01ns INFO     cocotb.regression                  gpio_mirror_test passed
10015090.01ns INFO     cocotb.regression                  ***************************************************************************************************
** TEST                                       STATUS  SIM TIME (ns)  REAL TIME (s)  RATIO (ns/s) **
***************************************************************************************************
** tb.test.gpio_mirror_test.gpio_mirror_test   PASS    10015090.01          63.84     156879.12  **
***************************************************************************************************
** TESTS=1 PASS=1 FAIL=0 SKIP=0                        10015090.01          65.07     153921.18  **
***************************************************************************************************
```

#### Fix: Building Program

On some machines you can get common makefile errors:

```
mkdir -p build/
riscv64-unknown-elf-gcc -march=rv32imc_zicsr -mabi=ilp32 -Wall -O2 -Os -Oz -nostdlib -nostartfiles -ffreestanding -fdata-sections -g  -Icore/inc -I/home/la_yk/MLAB_MCU_edu/uvm/sw/test/gpio/mirror/../../../../../uvm/sw/hal -I/home/la_yk/MLAB_MCU_edu/uvm/sw/test/gpio/mirror/../../../../../uvm/sw/soc -c main.c -o build/main.o
cc1: error: argument to '-O' should be a non-negative integer, 'g', 's' or 'fast'
cc1: error: '-march=rv32imc_zicsr': unsupported ISA subset 'z'
make: *** [/home/la_yk/MLAB_MCU_edu/uvm/sw/test/gpio/mirror/../../../../../sw/ibex/common/common.mk:81: build/main.o] Error 1
```


Apply common Makefile's patch:
```bash
patch ../sw/ibex/common/common.mk < ./patch/makefile.patch
```

And try running test again:
```bash
./script/init.sh --test
```

To reverse Makefile patch:
```bash
patch -R ../sw/ibex/common/common.mk < ./patch/makefile.patch
```

## Software

To build program:

```bash
cd sw/test/gpio/mirror
make
```
Clean build:

```bash
make clean && make
```

## Simulation

### Verilator

#### Dependencies

- [GTKWave](https://gtkwave.sourceforge.net/) for waveform viewing.

#### Build and Run

```bash
# You must be inside Python's Virtual Environment
source .venv/bin/activate
# Go to tb's Makefile location
cd sim/
# Build and Run
make
# Generate waveform file
make WAVES=1
# Clean cashed files
make clean
```

### Xcelium

#### Build and Run

```bash
# You must be inside Python's Virtual Environment
source .venv/bin/activate
# Go to tb's Makefile location
cd sim/
# Build and Run
make SIM=xcelium
# Clean cashed files
make SIM=xcelium clean
# Generate waveform file
make SIM=xcelium WAVES=1
# Run simulation in SimVision
make SIM=xcelium GUI=1
```