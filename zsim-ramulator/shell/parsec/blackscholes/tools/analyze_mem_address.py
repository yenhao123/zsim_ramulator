# -*- coding: utf-8 -*-

import pandas as pd

if __name__ == "__main__":
    file_name = "/root/ramulator-pim/zsim-ramulator/shell/parsec/blackscholes/tmp/memory_addresses_group.csv"
    df = pd.read_csv(file_name, header=None)
    df.columns = ['image_idx', 'MemoryAddress_otype', 'MemoryAddress_sptprice', 'MemoryAddress_strike', 'MemoryAddress_rate', 'MemoryAddress_volatility', 'MemoryAddress_otime']
    df[['MemoryAddress_otype', 'MemoryAddress_sptprice', 'MemoryAddress_strike', 
    'MemoryAddress_rate', 'MemoryAddress_volatility', 'MemoryAddress_otime']] = df[['MemoryAddress_otype', 'MemoryAddress_sptprice', 'MemoryAddress_strike', 
                                                                                   'MemoryAddress_rate', 'MemoryAddress_volatility', 'MemoryAddress_otime']].applymap(lambda x: int(x, 16))
    # 找到記憶體地址的最小值和最大值
    min_address, max_address = [], []
    for col in df.columns:
        if col == "image_idx":
            continue
        min_address.append(hex(df[col].min()))
        max_address.append(hex(df[col].max()))


    print("Memory Address Min:{}".format(min(min_address)))
    print("Memory Address Max:{}".format(max(max_address)))
    