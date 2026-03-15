module mcu #(
    parameter GPIO_COUNT        = `GPIO_IOS,
    parameter MEMInitFile       = `MEM_HEX_FILE,
    parameter IMEM_1_InitFile   = `IMEM1_HEX_FILE,
    parameter IMEM_2_InitFile   = `IMEM2_HEX_FILE,
    parameter DMEM_InitFile     = `DMEM_HEX_FILE
)(
    input  logic                    clk,
    input  logic                    rst,
    
    inout  wire [GPIO_COUNT-1:0]    ext_pad_io
);

    logic [GPIO_COUNT-1:0] gpio_i, gpio_o, gpio_oe;

    logic [GPIO_COUNT-1:0] tb_gpio_o = '0;
    logic [GPIO_COUNT-1:0] tb_gpio_oe  = '0;

    logic scl_pad_i, scl_pad_o, scl_padoen_o;
    logic sda_pad_i, sda_pad_o, sda_padoen_o;

    tri SDA, SCL;

    assign SCL       = scl_padoen_o ? 1'bz : scl_pad_o;
    assign scl_pad_i = SCL;

    assign SDA       = sda_padoen_o ? 1'bz : sda_pad_o;
    assign sda_pad_i = SDA;

    pullup(SDA);
    pullup(SCL);

    genvar i;
    generate
        for (i = 0; i < GPIO_COUNT; i++) begin : gen_gpio

            // dut drives the pad
            assign ext_pad_io[i] = gpio_oe[i] ? gpio_o[i] : 1'bz;

            // top driving the pad
            assign ext_pad_io[i] = tb_gpio_oe[i] ? tb_gpio_o[i] : 1'bz;

            // dut reading the pad
            assign gpio_i[i]     = ext_pad_io[i];

            // weak pulldown
            pulldown(ext_pad_io[i]);
        end
    endgenerate

    ibex_simple_system #(
        .IMEM_1_InitFile(IMEM_1_InitFile),
        .IMEM_2_InitFile(IMEM_2_InitFile),
        .DMEM_InitFile(DMEM_InitFile)
    ) dut (
        .clk_sys      (clk),
        .rst_async_n  (rst),
        .scl_pad_i    (scl_pad_i),
        .scl_pad_o    (scl_pad_o),
        .scl_padoen_o (scl_padoen_o),
        .sda_pad_i    (sda_pad_i),
        .sda_pad_o    (sda_pad_o),
        .sda_padoen_o (sda_padoen_o),
        .ext_pad_i    (gpio_i),
        .gpio_o       (gpio_o),
        .gpio_oe      (gpio_oe)
    );

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