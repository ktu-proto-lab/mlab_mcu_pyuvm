`include "project_defs.svh"

module mcu #(
    parameter GPIO_COUNT        = `GPIO_IOS,
    parameter MEMInitFile       = `MEM_HEX_FILE,
    parameter IMEM_1_InitFile   = `IMEM1_HEX_FILE,
    parameter IMEM_2_InitFile   = `IMEM2_HEX_FILE,
    parameter DMEM_InitFile     = `DMEM_HEX_FILE
)(
    input  logic                    clk,
    input  logic                    rst,
    
    input  logic [GPIO_COUNT-1:0]   gpio_i, 
    output logic [GPIO_COUNT-1:0]   gpio_o, 
    output logic [GPIO_COUNT-1:0]   gpio_oe,

    input  logic                    sda_i,
    output logic                    sda_o,
    output logic                    sda_oe,

    input  logic                    scl_i,
    output logic                    scl_o,
    output logic                    scl_oe
);

    // -----------------------------------------------------------------------------------------------------------------
    // Ibex Core
    // -----------------------------------------------------------------------------------------------------------------
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

    // -----------------------------------------------------------------------------------------------------------------
    // EEPROM
    // -----------------------------------------------------------------------------------------------------------------
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

endmodule
