# Patches

## Required

## Platform specific

### `sw/ibex/common/common.mk`

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
