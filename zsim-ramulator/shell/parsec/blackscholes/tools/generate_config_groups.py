# -*- coding: utf-8 -*-

def modify_cfg_file(i):
    # 读取 cfg 文件内容
    with open('/root/ramulator-pim/zsim-ramulator/tests/blackscholes_groups.cfg', 'r') as file:
        filedata = file.read()

    # 替换占位符 {input1} 为实际的值
    new_data = filedata.replace('{input1}', 'parsec_option_data_{}.csv'.format(i))
    new_data = new_data.replace('{output1}', 'parsec_option_data_{}.csv'.format(i))
    new_data = new_data.replace('{mem_o_idx}', str(i))

    # 将修改后的内容写回 cfg 文件
    with open('/root/ramulator-pim/zsim-ramulator/tests/blackscholes/group/blackscholes_{}.cfg'.format(i), 'w') as file:
        file.write(new_data)

def main():
    import os
    os.makedirs("output", exist_ok=True)
    n_group = 2
    for i in range(n_group):
        modify_cfg_file(i)

if __name__ == "__main__":
    main()