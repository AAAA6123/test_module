Модуль в `test_module.sv`

Тестбенч в `tb/test_module_tb.py`, внутри файла определены тестовые данные.

Тестбенч написан в [cocotb](https://docs.cocotb.org/en/stable/), менеджер пакетов [uv](https://github.com/astral-sh/uv).

По умолчанию использует [Verilator](https://www.veripool.org/verilator/) в качестве симулятора.

```
uv sync 
uv run tb/test_module_tb.py
```