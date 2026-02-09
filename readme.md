# IBEX RISC-V Microcontroller UVM Testing Framework

## Setup

### 1. Dependencies

1. [Python v3](https://www.python.org/downloads/)
2. [Verilator (v5.036+)](https://verilator.org/guide/latest/install.html#git-quick-install)

### 2. Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv
# Activate venv
source .venv/bin/activate
# Important! Upgrade pip first
pip install --upgrade pip
# Install needed packages
pip intall -r conf/requirements.txt
# Exit venv
deactivate
```

### 3. Patching

Some files require compatibility edits, apply them running patcher script:

```bash
./patch/patcher.sh --apply
```
