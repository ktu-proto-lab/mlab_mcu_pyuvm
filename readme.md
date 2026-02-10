# IBEX RISC-V Microcontroller UVM Testing Framework

## Setup

### 1. Dependencies

- [Python v3](https://www.python.org/downloads/)

### 2. Python Virtual Environment

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

### 3. Patching

Some files require compatibility edits, apply them running patcher script:

```bash
./patch/patcher.sh --apply
```

## Simulation

As of 09.02.26, the cocotb test in `src/test/test.py` is pure nonsense, the current implementation just deals with integration of the MCU to the cocotb for testing the compatibility of MCU itself and Verilator.

### 1. Dependencies

- [Verilator (v5.036+)](https://verilator.org/guide/latest/install.html#git-quick-install)
- [GTKWave](https://gtkwave.sourceforge.net/)

### 2. Build and Run

```bash
# You must be inside Python's Virtual Environment
source .venv/bin/activate
# Go to tb's Makefile location
cd src/tb
# Build and Run
make
# Clear project
make clean
```

### 3. Waveform

After completed simulation, `dump.vcd` file is generated.

```bash
# To see waveforms use GTKWave
gtkwave dump.vcd &
```
