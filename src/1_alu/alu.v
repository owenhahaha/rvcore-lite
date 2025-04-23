// Module: alu.v

`include "./alu_op.vh"

module alu(
    input [31:0] A,
    input [31:0] B,
    input [3:0] ALUSel,
    output reg [31:0] Out
);

always@* begin
    case(ALUSel)
        `ALU_ADD: Out = A + B;
        `ALU_SUB: Out = A - B;
        `ALU_AND: Out = A & B;
        `ALU_OR:  Out = A | B;
        `ALU_XOR: Out = A ^ B;
        `ALU_SLL: Out = A << B[4:0];
        `ALU_SRL: Out = A >> B[4:0];
        `ALU_SRA: Out = $signed(A) >>> B[4:0];
        `ALU_SLT: Out = $signed(A) < $signed(B);
        `ALU_SLTU: Out = A < B;
    endcase
end

endmodule