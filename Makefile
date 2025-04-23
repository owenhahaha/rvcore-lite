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
	@echo "\nStep 1: Generating test patterns and golden data..."
	python3 tools/$(TEST)/gen_test.py

	@echo "\nStep 2: Compiling and running simulation..."
	$(IVERILOG) -I src/$(TEST) -o $(OUT) $(SRC) $(TB)
	$(VVP) $(OUT)

	@echo "\nStep 3: Verifying simulation output against golden data..."
	python3 tools/$(TEST)/verify_result.py

	@echo "\nStep 4: Copying vcd files to local..."
	cp /home/owen/rvcore-lite/sim/$(TEST).vcd /mnt/d/Owen/Project/waveform

clean:
	rm -f sim/*

.PHONY: all sim clean