import cocotb
import pytest
from pathlib import Path

from cocotb.triggers import RisingEdge
from cocotb.runner import get_runner
from cocotb.clock import Clock
from cocotb.regression import TestFactory  

simulator = "verilator"

tb_data = []

# Исходные примеры
tb_data.append({ "test_data" : [1, 2, 1, 2, 1, 2, 1], "golden_output" : [2, 1] })
tb_data.append({ "test_data" : [1, 2, 3, 4, 3, 2, 3, 4, 3, 4], "golden_output" : [3, 4, 2, 1] })
# Дополнительные тесты
tb_data.append({ "test_data" : [5, 5, 5, 5, 5], "golden_output" : [5] })
tb_data.append({ "test_data" : [1, 3, 1, 3], "golden_output" : [1, 3] })
tb_data.append({ "test_data" : [10, 20, 30, 20, 30, 10], "golden_output" : [30, 20, 10] })
tb_data.append({ "test_data" : [1, 2, 3, 4, 5], "golden_output" : [4, 3, 2, 1] })
tb_data.append({ "test_data" : [1, 2, 3, 4, 5, 6], "golden_output" : [5, 4, 3, 2] })
tb_data.append({ "test_data" : [0, 1, 0, 2, 0], "golden_output" : [2, 0, 1] })
tb_data.append({ "test_data" : [255, 254, 255, 253], "golden_output" : [255, 254] })
tb_data.append({ "test_data" : [1, 2, 3, 1, 2, 3, 4, 1, 2], "golden_output" : [1, 4, 3, 2] })
tb_data.append({ "test_data" : [1, 2, 3, 4, 5, 6, 7, 8], "golden_output" : [7, 6, 5, 4] })
tb_data.append({ "test_data" : [100, 200, 50, 75, 100], "golden_output" : [75, 50, 200, 100] })
tb_data.append({ "test_data" : [15, 25], "golden_output" : [15] })
tb_data.append({ "test_data" : [9, 9, 9, 9, 8, 7], "golden_output" : [8, 9] })
tb_data.append({ "test_data" : [0, 255, 128, 0, 255], "golden_output" : [0, 128, 255] })
tb_data.append({ "test_data" : [1, 1, 2, 1, 2, 3, 1, 2, 3, 4, 1, 2, 3, 4, 5], "golden_output" : [4, 3, 2, 1] })
tb_data.append({ "test_data" : [10, 20, 30, 40, 50, 60, 70], "golden_output" : [60, 50, 40, 30] })
tb_data.append({ "test_data" : [42], "golden_output" : [] })
tb_data.append({ "test_data" : [11, 22, 33, 44, 55], "golden_output" : [44, 33, 22, 11] })
tb_data.append({ "test_data" : [1, 2, 3, 2, 1], "golden_output" : [2, 3, 1] })
tb_data.append({ "test_data" : [255, 254, 253, 252, 251], "golden_output" : [252, 253, 254, 255] })


# вспомогательные функции
async def send_data(clk, input, data):
  for value in data:
    input.value = value
    await RisingEdge(clk)

async def read_outputs(dut, depth: int = 4):
    outputs = []
    for idx in range(depth):
        if getattr(dut, f"out_valid_{idx}").value:
            outputs.append(int(getattr(dut, f"out_{idx}").value))
    return outputs


# тестбенч, параметризированный
async def run_tb(dut, tb_data):
  clk = dut.clk_in
  cocotb.start_soon(Clock(clk, 10, units="ns").start())
  await RisingEdge(clk)

  dut.reset_in.value = 1
  await RisingEdge(clk)
  dut.reset_in.value = 0

  await send_data(clk, dut.data_in, tb_data["test_data"])
  output = await read_outputs(dut)

  assert tb_data["golden_output"] == output, "Mismatch between output data and expected data"


# генерация тестов из наборов тестовых данных
factory = TestFactory(run_tb)
factory.add_option(name = "tb_data", optionlist=tb_data)
factory.generate_tests()


# python cocotb runner, запуск и настройка симулятора
def test_test_module():
  param = {'DATA_W' : 8}

  hdl_toplevel = "test_module"
  py_test_module = "test_module_tb,"

  proj_path = Path(__file__).resolve().parent.parent
  verilog_sources = [proj_path / "test_module.sv"]

  runner = get_runner(simulator)
  runner.build(
         verilog_sources=verilog_sources,
         hdl_toplevel=hdl_toplevel,
         parameters=param,
         waves=True
      )

  runner.test(hdl_toplevel=hdl_toplevel, 
              test_module=py_test_module, 
              waves=True)

if __name__ == "__main__":
  pytest.main([__file__, '-s'])
