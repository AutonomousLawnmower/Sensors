`timescale 1ns / 1ps

module mux8to1(
    input logic [6:0]D0, D1, D2, D3, D4, D5, D6, D7,
    input logic [2:0] S,
    input logic reset,
    output logic [6:0]f
    );
  
  always_comb
  begin
    if (reset)
        f = 7'b0000001;
    else
        case (S)
            3'd0: begin f = D0; end
            3'd1: begin f = D1;end
            3'd2: begin f = D2;end
            3'd3: begin f = D3;end
            3'd4: begin f = D4; end
            3'd5: begin f = D5;end
            3'd6: begin f = D6;end
            3'd7: begin f = D7;end
            default: f = 7'b1111111;
        endcase
 end
 
 endmodule