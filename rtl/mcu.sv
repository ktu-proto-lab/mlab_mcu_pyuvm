`include "project_defs.svh"

module mcu #(
    parameter GPIO_COUNT  = `GPIO_IOS,
    parameter MEMInitFile = `MEM_HEX_FILE,

    parameter IMEM_1_InitFile = `IMEM1_HEX_FILE,
    parameter IMEM_2_InitFile = `IMEM2_HEX_FILE,
    parameter DMEM_InitFile = `DMEM_HEX_FILE
)(
    input  logic                    clk,
    input  logic                    rst,
    
    inout  wire [GPIO_COUNT-1:0]    ext_pad_io,
    inout  wire                     SDA,
    inout  wire                     SCL
);

    logic [GPIO_COUNT-1:0] gpio_i, gpio_o, gpio_oe;
    
    logic scl_i, scl_o, scl_oe_n;
    logic sda_i, sda_o, sda_oe_n;

    // -------------------------------------------------------------------------
    // Bidirectional Tri-state Logic
    // -------------------------------------------------------------------------
    
    assign SDA   = sda_oe_n ? 1'bz : sda_o;
    assign sda_i = SDA;

    assign SCL   = scl_oe_n ? 1'bz : scl_o;
    assign scl_i = SCL;

    genvar i;
    generate
        for (i = 0; i < GPIO_COUNT; i++) begin : gen_gpio_tristate
            assign ext_pad_io[i] = gpio_oe[i] ? gpio_o[i] : 1'bz;
            assign gpio_i[i]     = ext_pad_io[i];
        end
    endgenerate

    // -------------------------------------------------------------------------
    // Ibex Core
    // -------------------------------------------------------------------------
    ibex_simple_system #(
        .IMEM_1_InitFile(IMEM_1_InitFile),
        .IMEM_2_InitFile(IMEM_2_InitFile),
        .DMEM_InitFile(DMEM_InitFile)
    ) dut (
        .clk_sys      (clk),
        .rst_async_n  (rst),

        .scl_pad_i    (scl_i),
        .scl_pad_o    (scl_o),
        .scl_padoen_o (scl_oe_n),
        
        .sda_pad_i    (sda_i),
        .sda_pad_o    (sda_o),
        .sda_padoen_o (sda_oe_n),

        .ext_pad_i    (gpio_i),
        .gpio_o       (gpio_o),
        .gpio_oe      (gpio_oe)
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
    // Pullups / Pulldowns
    // -------------------------------------------------------------------------
    
    pullup(SDA);
    pullup(SCL);

    genvar j;
    generate
        for(j=0; j<GPIO_COUNT; j++) begin : gen_gpio_pd
            pulldown(ext_pad_io[j]);
        end
    endgenerate

endmodule
