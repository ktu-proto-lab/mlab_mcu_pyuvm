# IBEX RISC-V Microcontroller UVM Testing Framework

## Setup

### Project

#### Initial Setup

```bash
# Clone the main project
git clone https://github.com/dovydasliutkus/MLAB_riscv_mcu.git
cd MLAB_riscv_mcu
# Remove static 'uvm' submodule
rm -rf uvm
# Clone this repository
git clone https://github.com/ManfredasLamsargis/MLAB_riscv_mcu_uvm.git uvm
cd uvm
```

`main` branch is the stable one and `dev` can have unstable or broken code

#### Updating

```bash
# Update to latest pushed commits
git pull
```

### Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv
# Activate venv
source .venv/bin/activate
# Important! Upgrade pip first
pip install --upgrade pip
# Install needed packages
pip install -r conf/requirements.txt
# Exit venv
deactivate
```

### Patching

Some files require compatibility edits, apply them running patcher script:

```bash
./patch/patcher.sh --apply
```

## Software

As of 17.02.26, the only program that can be used to run in simulation is `sw/gpio`.
To compile and build this program:

```bash
cd sw/gpio
make
```

Clean build:

```bash
make clean && make all
```

## Simulation

### Verilator

#### Dependencies

- [Verilator (v5.036+)](https://verilator.org/guide/latest/install.html#git-quick-install)
- [GTKWave](https://gtkwave.sourceforge.net/)

#### Build and Run

```bash
# You must be inside Python's Virtual Environment
source .venv/bin/activate
# Go to tb's Makefile location
cd sim/verilator
# Build and Run
make
```

#### Options

**Clean Simulation**
To remove simulation artifacts:

```bash
make clean
```

**Waveforms**

Script does not generate waveform files by default for compatibility reasons, to enable use command:

```bash
make WAVES=1
```

To see waveforms use GTKWave:

```bash
gtkwave dump.vcd &
```

### Xcelium

#### Build and Run

```bash
# You must be inside Python's Virtual Environment
source .venv/bin/activate
# Go to tb's Makefile location
cd sim/xcelium
# Build and Run
make
```

##### Options

**Clean Simulation**
To remove simulation artifacts:

```bash
make clean
```

**Waveforms**

To capture waveforms:

```bash
make WAVES=1
```

**SimVision (GUI)**

To run in SimVision GUI (captures waveforms automatically too for the GUI itself):

```bash
make GUI=1
```

### Testbench

As of 17.02.26 the testbench monitors the `GPIO` pin outputs and passes when the `GPIO_PIN_0` is set to `1` by the loaded program.

Expected output:

```log
99000980.00ns INFO     ..b/agent/gpio/gpio_monitor.py(30) [uvm_test_top.env.agent.monitor]: GPIO current pin values = 0x0
100000990.00ns INFO     ..b/agent/gpio/gpio_monitor.py(30) [uvm_test_top.env.agent.monitor]: GPIO current pin values = 0x1
100000990.00ns INFO     ..b/agent/gpio/gpio_monitor.py(39) [uvm_test_top.env.agent.monitor]: FLAG: GPIO values changed from 0x0 to 0x1
100000990.00ns INFO     ..m/tb/test/gpio_basic_test.py(25) [uvm_test_top]: PASS: GPIO_PIN_0 is high, expected = 1, actual = 1
100000990.01ns INFO     cocotb.regression                  gpio_basic_test passed
100000990.01ns INFO     cocotb.regression                  **********************************************************************************************
                                                           ** TEST                                  STATUS  SIM TIME (ns)  REAL TIME (s)  RATIO (ns/s) **
                                                           **********************************************************************************************
                                                           ** test.gpio_basic_test.gpio_basic_test   PASS   100000990.01         734.06     136229.13  **
                                                           **********************************************************************************************
                                                           ** TESTS=1 PASS=1 FAIL=0 SKIP=0                  100000990.01         734.16     136211.78  **
                                                           **********************************************************************************************
```
