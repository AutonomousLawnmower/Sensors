module Ultrasonic_Sensor(
	input logic clk,
	input logic reset, 
	input logic echo,
	output logic trig,
	output logic [7:0] dataout,
	output logic timeout

);

    logic ticker;
    logic [31:0] counter, counter_cm, distance_cm;
    mod_m_counter  #(.M(1000000)) tick (.clk(clk), .reset(reset), .max_tick(ticker));


always@(posedge clk) 
begin

	if(reset) 
	begin
        counter <= 0;
	    distance_cm <= 0;
		counter_cm <= 0;
		timeout <= 0;
	end
	
	else 
	begin
        counter <= counter + 1;
		
		if(counter <= 200)
		begin
		  trig <= 1'b0;
		end
		
		else if(counter >= 1200) 
		begin 
			trig <= 1'b0;
		end
		
		else 
		begin
			trig <= 1'b1;
		end
		
		if(echo)
		begin
			counter_cm <= counter_cm + 1;
			if(counter_cm == 5831)
			begin
				counter_cm <= 0;
				distance_cm <= distance_cm + 1;
			end
		end
		

		if(ticker)
		begin
			if(distance_cm < 100) 
			begin
			    timeout <= 0;
				dataout <= distance_cm;
			end
			else 
			begin
			    timeout <= 1;
				dataout <= 0;
			end
		end
		
		if(counter == 10000000) 
		begin
			counter <= 0;
			counter_cm <= 0;
			distance_cm <= 0;
		end	

	end
end		

endmodule