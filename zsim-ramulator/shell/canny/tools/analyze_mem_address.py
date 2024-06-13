import pandas as pd

if __name__ == "__main__":
    file_name = "/root/ramulator-pim/zsim-ramulator/shell/canny/tmp/memory_addresses_sequence.csv"
    df = pd.read_csv(file_name, header=None)
    df.columns = ['image_idx', 'row', 'col', 'MemoryAddress']
    df["MemoryAddress"] = df["MemoryAddress"].apply(lambda x: int(x, 16))
    # 找到記憶體地址的最小值和最大值
    min_address = df['MemoryAddress'].min()
    max_address = df['MemoryAddress'].max()

    # 將最小值和最大值轉換回十六進制字符串
    min_address_hex = hex(min_address)
    max_address_hex = hex(max_address)

    print("Memory Address Min:{}".format(min_address_hex))
    print("Memory Address Max:{}".format(max_address_hex))
    