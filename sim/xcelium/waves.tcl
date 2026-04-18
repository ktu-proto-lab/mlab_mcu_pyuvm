# NOTE:     used by the root sim makefile for xcelium waveform dumping with WAVES=1.
#           can be opened using simvision: 'simvision sim/waves.shm &'.

# open the shm database
database -open waves -into waves.shm -default

# probe all signals
probe -create -shm -all -depth all

# hand control to cocotb
run

# exit when simulation is finished
exit
