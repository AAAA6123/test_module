module test_module
#(
  parameter DATA_W = 8
)
(
  input logic clk_in,
  input logic reset_in,
  input logic [(DATA_W - 1) : 0] data_in,

  output logic [(DATA_W - 1) : 0] out_0,
  output logic out_valid_0,
  output logic [(DATA_W - 1) : 0] out_1,
  output logic out_valid_1,
  output logic [(DATA_W - 1) : 0] out_2,
  output logic out_valid_2,
  output logic [(DATA_W - 1) : 0] out_3,
  output logic out_valid_3
);

  localparam ARRAY_SIZE = 4;

  logic [(DATA_W - 1) : 0] data_buf [(ARRAY_SIZE - 1) : 0];
  logic [(ARRAY_SIZE - 1) : 0] data_buf_valid;
  logic [(ARRAY_SIZE - 1) : 0] is_equal;
  logic [(ARRAY_SIZE - 1) : 0] should_shift;

  // ищем совпадения входных данных с сохраненными
  always_comb begin
    for (int i=0; i < ARRAY_SIZE; i++) begin
      is_equal[i] = (data_in == data_buf[i] && data_buf_valid[i] == 1'b1) ? 1'b1 : 1'b0;
    end
  end

  // выбираем какую часть регистров перезаписать
  // эквивалент преобразования 0001 -> 0001,  0010 -> 0011, 0100 -> 0111, 1000 -> 1111, 0000 -> 1111
  assign should_shift = is_equal | (is_equal - 1);

  // сдвиговый регистр с условием, сдвигает данные отмеченные should_shift
  always_ff @(posedge clk_in) begin
    if (reset_in) begin
      data_buf_valid <= 0;
      data_buf <= '{default: 0};
    end else begin
      data_buf[0] <= data_in;
      data_buf_valid[0] <= 1'b1;

      for (int i = 1; i < ARRAY_SIZE; i=i+1) begin
        if (should_shift[i] == 1'b1) begin
          data_buf[i] <= data_buf[i-1];
          data_buf_valid[i] <= data_buf_valid[i-1];
        end
      end
    end
  end

  assign out_0 = data_buf[0];
  assign out_1 = data_buf[1];
  assign out_2 = data_buf[2];
  assign out_3 = data_buf[3];
  assign out_valid_0 = data_buf_valid[0];
  assign out_valid_1 = data_buf_valid[1];
  assign out_valid_2 = data_buf_valid[2];
  assign out_valid_3 = data_buf_valid[3];

endmodule
