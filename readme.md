# IBEX RISC-V Microcontroller PyUVM Testing Framework

## Cloning the Project

### Project

#### Version v0.3
```bash
# Clone the root project
git clone --recurse-submodules https://github.com/ktu-proto-lab/MLAB_MCU_edu.git
# Enter 'uvm' project
cd MLAB_MCU_edu/uvm
# The submodule can be in the unatached HEAD state, checkout to v0.1
git checkout v0.3
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
The most reliable way is to use docker for running project inside a container. First, you need [Docker](https://www.docker.com/) or [Podman](https://podman.io/) installed on your system.

You also need to have [GNU Make](https://www.gnu.org/software/make/make.html) to manage images and containers.

If you have required tools installed, inside `uvm` folder run:

```bash
make image verilator
```

This may take several minutes, depending on your system and hardware.

**Note**: if the image building fails, try rebuilding it second time, sometimes cloning verilator from github fails on the first try.

Several compatibility patches need to be applied for the root project, run the same makefile script to apply these patches:

```bash
make patch apply
```

To setup Python Virtual Environment run this, not that this does not require python inside your machine, this is a setup from a containerized environment in docker.

```bash
make venv verilator
```

Finally, you can enter the working environment by:

```bash
make run verilator
```

If you were greeted with success message and your terminal header looks like this:

```
user@container-verilator:/home/mcu/uvm/sim$ 
```

You've set working environment successfully. You can use `help` for future reference:

```bash
make help
```

## Running test

You must be inside working environment container, when you are there, go to the simulation root directory:

```bash
cd sim
```

Use `make help` as a reference, but for quick checkup you can run:

```bash
make SIM=verilator TEST=command_test LOG=DEBUG
```

This may take several minutes in the first run, because Verilator is translating RTL to C++ and then compiling those files.

If you see something like this:
```
0.00ns INFO     cocotb.regression                  running CommandTest (1/1)
   0.00ns INFO     ../mcu/uvm/tb/test/mcu_test.py(53) [uvm_test_top]: system clock: 12.5ns
   0.00ns INFO     ../mcu/uvm/tb/test/mcu_test.py(55) [uvm_test_top]: system reset for 20 clock cycles
```

The test is running inside container without any probems.

To exit working environment container just type `exit`. Then every time you need to go back just use:

```bash
make run verilator
```

You do not need to reinitialize working environment again.

## Tmux

For this project, [tmux v.3.0+](https://github.com/tmux/tmux/wiki) to run and manage this project.

If you are using tmux or have already installed, there is simple script that will set up the workflow for this project. Run inside `uvm` directory:

```bash
./script/env.sh
```

You can use your mouse to switch panels or keyboard, to exit the tmux session use `Ctrl + B` then `Shift + X` to close all panels.

Your environment should look something like this:

![tmux terminal custom working environment](/doc/res/img/tmux_env.png)
