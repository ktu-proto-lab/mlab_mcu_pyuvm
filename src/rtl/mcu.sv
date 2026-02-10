`include "project_defs.svh"

module mcu #(
    parameter GPIO_COUNT = `GPIO_IOS,
    parameter MEMInitFile = `MEM_HEX_FILE
)(
    input  logic                    clk_sys,
    input  logic                    rst_sys_n,
    inout  wire [GPIO_COUNT-1:0]    ext_pad_io
);

    // -------------------------------------------------------------------------
    // Signals
    // -------------------------------------------------------------------------
    // I2C Wires
    wire SDA, SCL;
    
    // Tie off test mode
    logic test_mode;
    assign test_mode = 1'b0;

    // -------------------------------------------------------------------------
    // Microcontroller
    // -------------------------------------------------------------------------
    ibex_simple_system dut (
        .clk_sys_Pad    (clk_sys),
        .rst_sys_n_Pad  (rst_sys_n),  
        .SDA_Pad        (SDA),
        .SCL_Pad        (SCL),
        .ext_pad        (ext_pad_io),
        .test_mode_Pad  (test_mode)
    );

    // -------------------------------------------------------------------------
    // EEPROM
    // -------------------------------------------------------------------------
    M24CS512 #(
        .MEMInitFile(MEMInitFile)
    ) eeprom (
        .A0     (1'b0),
        .A1     (1'b0),
        .A2     (1'b0),
        .WP     (1'b0),
        .SDA    (SDA),
        .SCL    (SCL),
        .RESET  (1'b0)
    );

    // -------------------------------------------------------------------------
    // Board Level Physics (Pullups/Pulldowns)
    // -------------------------------------------------------------------------
    
    // I2C Pullups
    pullup(SDA);
    pullup(SCL);

    // GPIO Pulldowns
    genvar j;
    generate
        for(j=0; j<GPIO_COUNT; j++) begin : gen_gpio_pd
            pulldown(ext_pad_io[j]);
        end
    endgenerate

endmodule
