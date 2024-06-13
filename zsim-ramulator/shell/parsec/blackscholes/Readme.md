## Build Up

1. execute generate_input.py
2. execute generate_config.py
3. execute main.sh

generate_input.py
>生成 blackscholes 的 input
>output directory: zsim-ramulator/shell/parsec/blackscholes/input/

generate_config.py
>每個 input 生成一個 config
>output directory: zsim-ramulator/tests/blackscholes/

get_memtrace.sh
>執行每個 config 檔以得到 memtrace_sequence
>memtrace_sequence output directory: zsim-ramulator/shell/parsec/blackscholes/mem_trace/
>cpu output directory: zsim-ramulator/shell/parsec/blackscholes/output/