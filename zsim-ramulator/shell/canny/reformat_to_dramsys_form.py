import argparse
from pathlib import Path

def convert_to_dramsysformat_total(data):
    operation_map = {
        "L" : "read",
        "S" : "write",
    }
    
    new_lines = []
    addr_arr = []
    for _, line in enumerate(data):
        parts = line.split()
        addr_arr.append(int(parts[4]))
    
    base_addr = min(addr_arr)
    for j, line in enumerate(data):
        parts = line.split()
        operation = operation_map[parts[3]]
        addr = hex(int(parts[4]) - base_addr)
        new_line = "{}:\t{}\t{}\n".format(j, operation, addr)
        new_lines.append(new_line)
    
    return new_lines

def convert_to_dramsysformat(data_group, n_groups):
    operation_map = {
        "L" : "read",
        "S" : "write",
    }
    
    new_data_group = []
    for i in range(n_groups):
        new_lines = []
        addr_arr = []
        for _, line in enumerate(data_group[i]):
            parts = line.split()
            addr_arr.append(int(parts[4]))
        
        base_addr = min(addr_arr)
        for j, line in enumerate(data_group[i]):
            parts = line.split()
            operation = operation_map[parts[3]]
            addr = hex(int(parts[4]) - base_addr)
            new_line = "{}:\t{}\t{}\n".format(j, operation, addr)
            new_lines.append(new_line)

        new_data_group.append(new_lines)
    
    return new_data_group

def out_file(data_group, n_groups=10):
    for i in range(n_groups):
        with open("dramsys_mem_trace/dramsys_input_{}.stl".format(i), "w") as f:
            f.writelines(data_group[i])

if __name__ == "__main__":
    
    '''
    for example, python reformat_to_dramsys_form.py mem_trace/canny_0
    '''
    parser = argparse.ArgumentParser(description="Convert fifth column of input data to hexadecimal.")
    parser.add_argument("memtrace_path", type=str, help="Input data string, separated by newlines.")

    n_groups=50
    
    # Parse arguments
    args = parser.parse_args()
    with Path(args.memtrace_path).open("r") as f:
        data = f.readlines()
    
    # record all data
    new_data = convert_to_dramsysformat_total(data)
    with open("dramsys_mem_trace/dramsys_input_all.stl", "w") as f:
        f.writelines(new_data)

    # spilit to n groups
    data_group = []
    for i in range(n_groups):
        data_group.append(data[i*(len(data)//n_groups):(i+1)*(len(data)//n_groups)])
     
    data_group = convert_to_dramsysformat(data_group, n_groups)
    out_file(data_group, n_groups)