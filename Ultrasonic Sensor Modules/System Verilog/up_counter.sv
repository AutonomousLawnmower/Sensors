`timescale 1ns / 1ps

module upcounter (reset, clk, Q, en);
	input logic reset, clk, en;
	output logic [2:0] Q;
	
	always_ff @(posedge clk)
	 	if (reset)
			Q <= 0;
		else 
		if(en)
		begin
			Q <= Q + 1;
	    end
	    else
	       Q <= Q;
endmodule