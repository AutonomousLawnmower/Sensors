`timescale 1ns / 1ps
 module three_to_eight_decoder(
    input logic reset,
    input logic [2:0] data,
    output logic [7:0] y
    );
 
 always_comb
 begin
    if(reset)
    begin y = 8'd0; end
    else
    case(data)
        3'd0: begin y = 8'b11111110;  end
        3'd1: begin y = 8'b11111101;  end
        3'd2: begin y = 8'b11111011; end
        3'd3: begin y = 8'b11110111;  end
        3'd4: begin y = 8'b11101111;  end
        3'd5: begin y = 8'b11011111;  end
        3'd6: begin y = 8'b10111111; end
        3'd7: begin y = 8'b01111111;  end
        default: begin y = 8'b11111111; end
	endcase
end

endmodule