import argparse
from pathlib import Path

#4G
DRAM_CAPACITY = 4294967295
BASE_ADDR = 536870912
N_REPLAY = 100
def convert_to_dramsysformat_total(data):
    operation_map = {
        "L" : "read",
        "S" : "write",
    }
    
    new_lines = []
    prev_addr = 0
    for j, line in enumerate(data):
        parts = line.split()
        operation = operation_map[parts[3]]
        ori_addr = int(parts[4])
        offset = ori_addr - prev_addr
        prev_addr = ori_addr
        if j == 0:
            continue

        if abs(offset) > BASE_ADDR:
            addr = hex(BASE_ADDR * 2)
        else:
            addr = hex(BASE_ADDR + offset)
        
        new_line = "{}:\t{}\t{}\n".format(j, operation, addr)
        new_lines.append(new_line)
    
    return new_lines

def convert_to_dramsysformat_total_replay(data):
    operation_map = {
        "L" : "read",
        "S" : "write",
    }
    
    new_items = []
    prev_addr = 0
    for j, line in enumerate(data):
        parts = line.split()
        operation = operation_map[parts[3]]
        ori_addr = int(parts[4])
        offset = ori_addr - prev_addr
        prev_addr = ori_addr
        if j == 0:
            continue

        if abs(offset) > BASE_ADDR:
            addr = hex(BASE_ADDR * 2)
        else:
            addr = hex(BASE_ADDR + offset)
        
        new_items.append((operation, addr))
        
    new_items_replay = []
    for _ in range(N_REPLAY):
        new_items_replay += new_items
    
    new_lines = []
    for j, item in enumerate(new_items_replay):
        operation, addr = item
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
        prev_addr = 0
        for j, line in enumerate(data_group[i]):
            parts = line.split()
            operation = operation_map[parts[3]]
            ori_addr = int(parts[4])
            offset = ori_addr - prev_addr
            prev_addr = ori_addr
            if j == 0:
                continue
            if abs(offset) > BASE_ADDR:
                addr = hex(BASE_ADDR * 2)
            else:
                addr = hex(BASE_ADDR + offset)
                         
            new_line = "{}:\t{}\t{}\n".format(j, operation, addr)
            new_lines.append(new_line)

        new_data_group.append(new_lines)
    
    return new_data_group

def convert_to_dramsysformat_replay(data_group, n_groups):
    operation_map = {
        "L" : "read",
        "S" : "write",
    }
    
    new_data_group = []
    for i in range(n_groups):
        new_items = []
        prev_addr = 0
        for j, line in enumerate(data_group[i]):
            parts = line.split()
            operation = operation_map[parts[3]]
            ori_addr = int(parts[4])
            offset = ori_addr - prev_addr
            prev_addr = ori_addr
            if j == 0:
                continue
            if abs(offset) > BASE_ADDR:
                addr = hex(BASE_ADDR * 2)
            else:
                addr = hex(BASE_ADDR + offset)
                         
            new_items.append((operation, addr))
        
        new_items_replay = []
        for _ in range(N_REPLAY):
            new_items_replay += new_items
        
        new_lines = []
        for j, item in enumerate(new_items_replay):
            operation, addr = item
            new_line = "{}:\t{}\t{}\n".format(j, operation, addr)
            new_lines.append(new_line)
        
        new_data_group.append(new_lines)
    
    return new_data_group

def out_file(data_group, n_groups):
    for i in range(n_groups):
        with open("/root/ramulator-pim/zsim-ramulator/shell/canny/dramsys_mem_trace/n_groups={}/dramsys_input_{}.stl".format(n_groups, i), "w") as f:
            f.writelines(data_group[i])

def out_file_replay(data_group, n_groups):
    for i in range(n_groups):
        with open("/root/ramulator-pim/zsim-ramulator/shell/canny/dramsys_mem_trace/n_groups={}/dramsys_input_{}_replay.stl".format(n_groups, i), "w") as f:
            f.writelines(data_group[i])

if __name__ == "__main__":
    
    '''
    for example, python reformat_to_dramsys_form.py mem_trace/canny_0
    '''
    parser = argparse.ArgumentParser(description="Convert fifth column of input data to hexadecimal.")
    parser.add_argument("--memtrace_path", type=str, required=True, help="Input data string, separated by newlines.")
    parser.add_argument("--groups", type=int, required=True, help="Input data string, separated by newlines.")
    args = parser.parse_args()
    n_groups=args.groups
    
    with Path(args.memtrace_path).open("r") as f:
        data = f.readlines()
    
    # record all data
    new_data = convert_to_dramsysformat_total(data)
    with open("/root/ramulator-pim/zsim-ramulator/shell/canny/dramsys_mem_trace/n_groups={}/dramsys_input_all.stl".format(n_groups), "w") as f:
        f.writelines(new_data)

    # spilit to n groups
    data_group = []
    for i in range(n_groups):
        data_group.append(data[i*(len(data)//n_groups):(i+1)*(len(data)//n_groups)])
     
    data_group = convert_to_dramsysformat(data_group, n_groups)
    out_file(data_group, n_groups)


    # record all data (replay) 
    new_data = convert_to_dramsysformat_total_replay(data)
    with open("/root/ramulator-pim/zsim-ramulator/shell/canny/dramsys_mem_trace/n_groups={}/dramsys_input_all_replay.stl".format(n_groups), "w") as f:
        f.writelines(new_data)

    # spilit to n groups (replay)     
    data_group = []
    for i in range(n_groups):
        data_group.append(data[i*(len(data)//n_groups):(i+1)*(len(data)//n_groups)])
    
    data_group = convert_to_dramsysformat_replay(data_group, n_groups)
    out_file_replay(data_group, n_groups)