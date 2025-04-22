# Makefile

IVERILOG = iverilog
TEST = 1_alu
VVP = vvp
GTK = gtkwave
SRC = src/$(TEST)/*.v
TB = tb/$(TEST)/*.v
OUT = sim/$(TEST)
VCD = sim/$(TEST).vcd

all: sim

sim:
	$(IVERILOG) -I src/$(TEST) -o $(OUT) $(SRC) $(TB)
	$(VVP) $(OUT)
	cp /home/owen/rvcore-lite/sim/$(TEST).vcd /mnt/d/Owen/Project/waveform

clean:
	rm -f sim/*

.PHONY: all sim clean