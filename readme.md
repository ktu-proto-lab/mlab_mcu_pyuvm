# IBEX RISC-V Microcontroller UVM Testing Framework

## Cloning the Project

### Project

#### Version v0.1
```bash
# Clone the root project
git clone --recurse-submodules https://github.com/dovydasliutkus/MLAB_MCU_edu.git
# Enter 'uvm' project
cd MLAB_MCU_edu/uvm
# The submodule can be in the unatached HEAD state, checkout to v0.1
git checkout v0.1
```

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
user@mlab:/home/mcu/uvm
```
Use to run simulations, compile code, generate reports. Local files are linked with the container, edit files from your local machine, do not edit them inside the docker, that is general tip.

### Python's Virtual Environment

When the setup is completed, run second project initialization step (run script inside the Docker container if you are using it):

```bash
./script/init.sh --env
```

### Run tests
There are 2 tests for GPIO and UART peripheral each. You must run make inside the `sim` folder.
To run on Verilator:
```bash
# terminal-only
make TEST=gpio_simple_test LOG=INFO
# clean sim_build directory
make clean
# dump vcd's example
make TEST=uart_simple_test LOG=DEBUG WAVES=1
```
To run on Cadence Xcelium
```bash
make SIM=xcelium TEST=gpio_simple_test LOG=DEBUG
make SIM=xcelium clean
make SIM=xcelium TEST=uart_simple_test GUI=1
```
