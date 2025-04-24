# RISC-V Central Processor Unit (CPU) Design

<p align="right">
Owen Chen
</p>

This is a side project aimed at implementing a RISC-V-based CPU in Verilog, entirely from scratch. The initial goal is to build a working single-cycle CPU that supports the basic RV32I instruction set. Over time, the design will progressively evolve into a more complex system, including multi-stage pipelining, cache hierarchy, and software integration.

Through this project, I hope to gain deeper experience in RTL design, simulation, and verification. Additionally, this project serves as a hands-on journey to better understand modern processor architecture, memory subsystems, and low-level software interaction — including running compiled C programs and supporting simple operating system features.

Ultimately, this project is not just about building a CPU, but also about integrating my knowledge in digital design with real development workflows using Linux, Git, and Python-based tooling.

This project is divided into six progressive phases:

1. **RISC-V ALU (Arithmetic Logic Unit)**  
   Implement a 32-bit ALU that supports all basic arithmetic and logical operations defined in the RV32I base instruction set.

2. **Single-Cycle RISC-V CPU**  
   Build a basic CPU that executes one instruction per clock cycle, supporting instruction fetch, decode, execute, memory access, and write-back in a single stage.

3. **Pipelined 5-Stage RISC-V CPU**  
   Introduce instruction-level parallelism by separating the CPU into five stages (IF, ID, EX, MEM, WB), along with hazard detection and forwarding logic.

4. **Cache and Memory Hierarchy**  
   Design a simple instruction and data cache system, and explore the concept of memory hierarchy to improve performance.

5. **Software Integration: Running C Programs**  
   Integrate a RISC-V GCC toolchain to compile C programs into machine code that can run on the custom CPU. Learn how to load and execute binaries, manage stack and memory layout, and support basic system calls (e.g., `putchar`, `exit`).

6. **Minimal Operating System / Runtime Environment**  
   Build a basic task loader or minimal operating system environment, enabling features like context switching, system-level debugging, and simple I/O.

Each phase is designed to build upon the previous one, gradually transforming the CPU into a more complete and realistic RISC-V system. The goal is not only to strengthen my Verilog and RTL design skills, but also to gain a system-level perspective from hardware to software.


### File Structure

```bash
rvcore-lite/
├── src/1_alu/        # Verilog RTL
├── tb/               # Testbench
├── sim/              # Simulation output files (text, waveform)
├── tools/            # Python tools (random input generation, verification)
├── test_prog/        # Verification code (ASM, compiled C)
├── Makefile          # Automate simulation flow
├── README.md         # Project introduction
└── .gitignore        
```
<br><br><br>

---

## Phase 1: RISC-V ALU (Arithmetic Logic Unit)

This is a simple Arithmetic Logic Unit (ALU) implemented in Verilog, following the RISC-V specification. It supports basic arithmetic and bitwise operations, and is intended as part of a single-cycle RISC-V CPU project.

`ALU` module has two 32-bit inputs `A`, `B` for the numbers to be computed, and a 5-bit input `ALUSel` as the operation selection signal, the output of `ALU` is the calculated 32-bit result.

### Features
- Support the following operations:
  - Addition (`add`)
  - Subtraction (`sub`)
  - Bitwise AND (`and`)
  - Bitwise OR (`or`)
  - Bitwise XOR (`xor`)
  - Shift Left Logical (`sll`)
  - Shift Right Logical (`srl`)
  - Shift Right Arithmetic (`sra`)
  - Set Less Than (Signed) (`slt`)
  - Set Less Than (Unsigned) (`sltu`)

### Simulation & Verification

1. Generate random input patterns/golden data with python.
2. Testbench simulation with generated input, output result data.
3. Verification with python by comparing result and golden data.

### File
```bash
# source file
 - src/1_alu/alu.v
 - src/1_alu/alu_op.vh

# testbench simulation
 - tb/1_alu/alu_tb.v

# python verification
 - tools/1_alu/gen_test.py
 - tools/1_alu/verify_result.py
 - sim/1_alu_test.txt
 - sim/1_alu_golden.txt

# simulation output
 - sim/1_alu_result.txt
 - sim/1_alu.vcd
```
<br><br><br>

---

## Phase 2: Single-cycle RISC-V CPU

This initial RISC-V CPU design aims for single-cycle instruction execution, without optimizing critical path. The primary objective of this stage is to implement a functional CPU supporting the specified RV32I instruction set.

RV32I Instruction Set
- Integer Register-Register Instructions

| Instruction | Description | Type | Opcode | Funct3 | Funct7 |
| :----------: | :---------- | :--: | :----: | :----: | :----: |
| add  rd rs1 rs2 | R[rd] = R[rs1] + R[rs2] | R | 011 0011 | 000 | 000 0000 |
| sub  rd rs1 rs2 | R[rd] = R[rs1] - R[rs2] | R | 011 0011 | 000 | 010 0000 |
| and  rd rs1 rs2 | R[rd] = R[rs1] & R[rs2] | R | 011 0011 | 111 | 000 0000 |
| or  rd rs1 rs2 | R[rd] = R[rs1] \| R[rs2] | R | 011 0011 | 110 | 000 0000 |
| xor  rd rs1 rs2 | R[rd] = R[rs1] ^ R[rs2] | R | 011 0011 | 100 | 000 0000 |
| sll  rd rs1 rs2 | R[rd] = R[rs1] << R[rs2] | R | 011 0011 | 001 | 000 0000 |
| srl  rd rs1 rs2 | R[rd] = R[rs1] >> R[rs2]<br>(Zero-extended) | R | 011 0011 | 101 | 000 0000 |
| sra  rd rs1 rs2 | R[rd] = R[rs1] >> R[rs2]<br>(Sign-extended) | R | 011 0011 | 101 | 010 0000 |
| slt  rd rs1 rs2 | if (R[rs1] < R[rs2]) R[rd] = 1;<br>else R[rd] = 0;<br>(signed-comparison) | R | 011 0011 | 010 | 000 0000 |
| sltu  rd rs1 rs2 | if (R[rs1] < R[rs2]) R[rd] = 1;<br>else R[rd] = 0;<br>(unsigned-comparison) | R | 011 0011 | 011 | 000 0000 |

- Integer Register-Immediate Instructions:

| Instruction | Description | Type | Opcode | Funct3 | Funct7 |
| :----------: | :---------- | :--: | :----: | :----: | :----: |
| addi  rd rs1 imm | R[rd] = R[rs1] + imm | I | 001 0011 | 000 |   |
| andi  rd rs1 imm | R[rd] = R[rs1] & imm | I | 001 0011 | 111 |   |
| ori  rd rs1 imm | R[rd] = R[rs1] \| imm | I | 001 0011 | 110 |   |
| xori  rd rs1 imm | R[rd] = R[rs1] ^ imm | I | 001 0011 | 100 |   |
| slli  rd rs1 imm | R[rd] = R[rs1] << imm | I* | 001 0011 | 001 | 000 0000 |
| srli  rd rs1 imm | R[rd] = R[rs1] >> imm<br>(Zero-extended) | I* | 001 0011 | 101 | 000 0000 |
| srai  rd rs1 imm | R[rd] = R[rs1] >> imm<br>(Sign-extended) | I* | 001 0011 | 101 | 010 0000 |
| slti  rd rs1 imm | if (R[rs1] < imm) R[rd] = 1;<br>else R[rd] = 0;<br>(signed-comparison) | I | 001 0011 | 010 |   |
| sltiu  rd rs1 imm | if (R[rs1] < imm) R[rd] = 1;<br>else R[rd] = 0;<br>(unsigned-comparison) | I | 001 0011 | 011 |   |

- Load/Store Instructions:

| Instruction | Description | Type | Opcode | Funct3 |
| :----------: | :---------- | :--: | :----: | :----: |
| lb  rd imm(rs1) | R[rd] = M[R[rs1] + imm][7:0]<br>(Sign-extended) | I | 000 0011 | 000 |
| lbu  rd imm(rs1) | R[rd] = M[R[rs1] + imm][7:0]<br>(Zero-extended) | I | 000 0011 | 100 |
| lh  rd imm(rs1) | R[rd] = M[R[rs1] + imm][15:0]<br>(Sign-extended) | I | 000 0011 | 001 |
| lhu  rd imm(rs1) | R[rd] = M[R[rs1] + imm][15:0]<br>(Zero-extended) | I | 000 0011 | 101 |
| lw  rd imm(rs1) | R[rd] = M[R[rs1] + imm][31:0]| I | 000 0011 | 010 |
| sb  rs2 imm(rs1) | M[R[rs1] + imm][7:0] = R[rs2][7:0]| S | 010 0011 | 000 |
| sh  rs2 imm(rs1) | M[R[rs1] + imm][15:0] = R[rs2][15:0]| S | 010 0011 | 001 |
| sw  rs2 imm(rs1) | M[R[rs1] + imm][31:0] = R[rs2][31:0]| S | 010 0011 | 010 |

- Branch Instructions:

| Instruction | Description | Type | Opcode | Funct3 |
| :----------: | :---------- | :--: | :----: | :----: |
| beq  rs1 rs2 label | if (R[rs1] == R[rs2])<br>PC = PC + offset | B | 110 0011 | 000 |
| bne  rs1 rs2 label | if (R[rs1] != R[rs2])<br>PC = PC + offset | B | 110 0011 | 001 |
| blt  rs1 rs2 label | if (R[rs1] < R[rs2])<br>PC = PC + offset<br>(signed-comparison) | B | 110 0011 | 100 |
| bltu  rs1 rs2 label | if (R[rs1] < R[rs2])<br>PC = PC + offset<br>(unsigned-comparison) | B | 110 0011 | 110 |
| beg  rs1 rs2 label | if (R[rs1] >= R[rs2])<br>PC = PC + offset<br>(signed-comparison) | B | 110 0011 | 101 |
| begu  rs1 rs2 label | if (R[rs1] >= R[rs2])<br>PC = PC + offset<br>(unsigned-comparison) | B | 110 0011 | 111 |

- Jump Instructions:

| Instruction | Description | Type | Opcode | Funct3 |
| :----------: | :---------- | :--: | :----: | :----: |
| jal  rd label | R[rd] = PC + 4<br>PC = PC + offset | J | 110 1111 |   |
| jalr  rd rs1 imm | R[rd] = PC + 4<br>PC = R[rs1] + imm | I | 110 0111 | 000 |

- Upper Immediate Instructions:

| Instruction | Description | Type | Opcode |
| :----------: | :---------- | :--: | :----: |
| auipc rd immu | imm = immu << 12<br>R[rd] = PC + imm | U | 001 0111 |
| lui  rd immu | imm = immu << 12<br>R[rd] = imm | U | 011 0111 |

- System Environment Call and Breakpoints:

| Instruction | Description | Type | Opcode | Funct3 |
| :----------: | :---------- | :--: | :----: | :----: |
| ecall | Triggers a system call to request services from the OS or runtime<br>(imm = 0) | I | 111 0011 | 000 |
| ebreak | Triggers a breakpoint exception, typically used by debuggers to halt execution<br>(imm = 1) | I | 111 0011 | 000 |

