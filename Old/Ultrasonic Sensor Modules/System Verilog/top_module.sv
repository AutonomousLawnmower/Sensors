`timescale 1ns / 1ps

module top(
    input logic CLK, RESET,ECHO1, ECHO2, ECHO3, ECHO4,
    input logic [1:0] us_select,
    output logic TIMEOUT, TRIG1, TRIG2, TRIG3, TRIG4,
    output logic [7:0] LED,
    output logic [7:0] AN,
    output logic [6:0] C,
    output logic DP,
    output logic [7:0] DATA
    );
    assign DP = 1;
    logic nextBit;
    logic [7:0] data_out;
    logic clock_400hz;
    logic [2:0] count;
    logic [6:0] D0,D1,D2,D3,D4,D5,D6,D7;
    logic [7:0] data_us1, data_us2, data_us3, data_us4;
    logic t1,t2,t3,t4;
    logic [7:0] sseg;
    
    
    mod_m_counter #(.M(125_000)) sc (.clk(CLK), .reset(RESET), .max_tick(clock_400hz));
     
    upcounter myupcounter (.clk(CLK), .en(clock_400hz), .reset(RESET),.Q(count));
     
    three_to_eight_decoder mydecoder (.reset(RESET), .data(count), .y(AN));
     
    seven_seg_decoder mysseg (.dataout(sseg), .D0(D0),
    .D1(D1),.D2(D2),.D3(D3),.D4(D4),.D5(D5),.D6(D6),.D7(D7));
     
    mux8to1 mymux (.reset(RESET),.D0(D0), .S(count), .D1(D1),.D2(D2),.D3(D3),
    .D4(D4),.D5(D5),.D6(D6),.D7(D7), .f(C));
    
    
    Ultrasonic_Sensor us1(CLK, RESET, ECHO1, TRIG1, data_us1, t1);
    Ultrasonic_Sensor us2(CLK, RESET, ECHO2, TRIG2, data_us2, t2);
    Ultrasonic_Sensor us3(CLK, RESET, ECHO3, TRIG3, data_us3, t3);
    Ultrasonic_Sensor us4(CLK, RESET, ECHO4, TRIG4, data_us4, t4);
    
    
    //rising_edge (CLK, RESET, NEXT, nextBit);
    //adapter(CLK, RESET, LOAD, nextBit, us_data, SOUT, data_out);
    
    assign sseg = us_select[1] ? (us_select[0]?data_us4:data_us3):(us_select[0]?data_us2:data_us1);
    assign LED = us_select[1] ? (us_select[0]?data_us4:data_us3):(us_select[0]?data_us2:data_us1);
    assign DATA = us_select[1] ? (us_select[0]?data_us4:data_us3):(us_select[0]?data_us2:data_us1);
    assign TIMEOUT = us_select[1] ? (us_select[0]?t4:t3):(us_select[0]?t2:t1);
    
endmodule
