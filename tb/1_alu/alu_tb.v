`timescale 1ns / 1ps

module alu_tb();

reg clk;
reg [31:0] a;
reg [31:0] b;
reg [3:0] sel;
wire [31:0] out;

alu U_alu(
    .A(a),
    .B(b),
    .ALUSel(sel),
    .Out(out)
);

integer fin, fout;

// clock signal generator
initial clk = 0;
always #0.5 clk = ~clk;

// dump wave file
initial begin
    $dumpfile("sim/1_alu.vcd");
    $dumpvars(0, alu_tb);
end

// simulation
// initial begin
//     fin = $fopen("sim/alu_test.txt", "r");
//     fout = $fopen("sim/alu_result.txt", "w");

//     while (!$feof(fin)) begin
//         $fscanf(fin, "%h %h %h\n", a, b, sel);
//         #0.5;
//         $fwrite(fout, "%08x\n", out);
//         #0.5;
//     end
//     $fclose(fin);
//     $fclose(fout);
//     $finish();
// end

// simulation
integer i, j;

initial begin
    sel = 4'd0;
    fout = $fopen("sim/1_alu.out", "w");

    for(i=0; i<10; i=i+1) begin
        for(j=22; j<32; j=j+1) begin
            a = i;
            b = $signed(j);
            #0.5;
            // $fwrite(fout, "%08x, %08x, %08x\n", a, b, out);
            $fwrite(fout, "a = %2d; b = %2d; out = %2d\n", a, b, out);
            #0.5;
        end
    end
    $fclose(fout);
    $display("##### End of Simulation #####");
    $finish();
end

endmodule