# IbexBranchDecisionValid Assert Failure
Last edited on 18.04.26 by Manfredas Lamsargis.

When running one test, one of the core asserts fail on xcelium:
```
xmsim: *E,ASRTST (/home/mcu/rtl/core/ibex_id_stage.sv,1142): (time 112175 NS) Assertion mcu.dut.u_wb_ibex_top.inst_ibex_top.u_ibex_core.id_stage_i.IbexBranchDecisionValid has failed
112175000: (/home/mcu/rtl/core/ibex_id_stage.sv:1142) [mcu.dut.u_wb_ibex_top.inst_ibex_top.u_ibex_core.id_stage_i.IbexBranchDecisionValid] [ASSERT FAILED] IbexBranchDecisionValid
```

# Reproduce
If running the first time, you need to add this in your `~/.config/containers/storage.conf`:
```
# ~/.config/containers

[storage]
driver = "overlay"

[storage.options]
ignore_chown_errors = "true"
```

Workflow to reproduce assert:
```bash
# delete if there are any old images
make image xcelium purge
# build image
make image xcelium
# remove old
rm -rf .venv/
# build venv
make venv xcelium
# enter xcelium container
make run xcelium
# activate virtual environment
source .venv/bin/activate
# enter simulation folder
cd sim
# run root make with these arguments
make SIM=xcelium TEST=gpio_wiggle_simple_test LOG=DEBUG WAVES=1
# when done exit the container
exit
# see the waveform of the pyuvm test
simvision sim/waves.shm/ &
```