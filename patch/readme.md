# Patches

## Required

### Verilator

#### EEPROM `tb/misc/24CS512.sv` patch

_last checked on 24.02.26_

Running on Verilator from the Makefile in `sim/verilator` directory you get these C++ generated code errors:

```
Vtop___024root__0__Slow.cpp:23:15: error: ‘class Vtop___024root’ has no member named ‘mcu__DOT__eeprom__DOT__tHS_HI’; did you mean ‘mcu__DOT__eeprom__DOT__MAN_ID’?
   23 |     vlSelfRef.mcu__DOT__eeprom__DOT__tHS_HI = 60.0;
      |               ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      |               mcu__DOT__eeprom__DOT__MAN_ID
Vtop___024root__0__Slow.cpp:24:15: error: ‘class Vtop___024root’ has no member named ‘mcu__DOT__eeprom__DOT__tHS_LO’; did you mean ‘mcu__DOT__eeprom__DOT__MAN_ID’?
   24 |     vlSelfRef.mcu__DOT__eeprom__DOT__tHS_LO = 160.0;
      |               ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~
```

There is more than two of them, this is C++ generator specific issue, where it generates signal fields as private and then cocotb requires expose all signal values to the dut's interface (not guaranteed, but yeah).

Apply the patch for the EEPROM misc file (from the `~/MLAB_MCU_edu`):

```bash
patch -Nfs -V none -r - ./tb/misc/24CS512.sv < ./uvm/patch/eeprom.patch
```

Clean the cashed files (because the same errors will occur) and run make again:

```bash
make clean && make
```

## Platform specific

### Makefile compile flags `sw/ibex/common/common.mk` patch

_last checked on 23.02.26_

On some platforms the common makefile `common.mk` in the root project in `sw/ibex/common` may not work with current compiler flags. The error that can be seen looks familiar to this:

```
$ make
mkdir -p build/
riscv64-unknown-elf-gcc -march=rv32imc_zicsr -mabi=ilp32 -Wall -O2 -Os -Oz -nostdlib -nostartfiles -ffreestanding -fdata-sections -g  -Icore/inc -c core/src/main.c -o build/main.o
cc1: error: argument to '-O' should be a non-negative integer, 'g', 's' or 'fast'
cc1: error: '-march=rv32imc_zicsr': unsupported ISA subset 'z'
make: *** [/home/la_52/MLAB_MCU_edu/uvm/sw/gpio/../../../sw/ibex/common/common.mk:81: build/main.o] Error 1
```

Apply `patch/sw_common_makefile.patch` from the `~/MLAB_MCU_edu` root project directory to get rid of incompatible compile flags:

```bash
patch -Nfs -V none -r - ./sw/ibex/common/common.mk < ./uvm/patch/sw_common_makefile.patch
```
