
def modify_cfg_file(i):
    # 读取 cfg 文件内容
    with open('/root/ramulator-pim/zsim-ramulator/tests/canny_group.cfg', 'r') as file:
        filedata = file.read()

    # 替换占位符 {input1} 为实际的值
    new_data = filedata.replace('{group_idx}', str(i))

    # 将修改后的内容写回 cfg 文件
    with open('/root/ramulator-pim/zsim-ramulator/tests/canny/group/canny_{}.cfg'.format(i), 'w') as file:
        file.write(new_data)

def main():
    import os
    os.makedirs("output", exist_ok=True)
    n_group = 1
    for i in range(n_group):
        modify_cfg_file(i)

if __name__ == "__main__":
    main()