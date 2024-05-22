import csv
import random

# 生成期权数据
def generate_option_data(num_rows):
    data = []
    for _ in range(num_rows):
        current_price = round(random.uniform(10, 150), 2)  # 当前股价
        strike_price = round(random.uniform(10, 150), 2)   # 行权价格
        volatility = round(random.uniform(0.01, 0.5), 4)   # 波动率
        dividend_yield = round(random.uniform(0.0, 0.05), 2) # 股息收益率
        risk_free_rate = round(random.uniform(0.01, 0.2), 2) # 无风险利率
        time_to_maturity = round(random.uniform(0.1, 2.0), 2) # 到期时间
        option_type = random.choice(['C', 'P'])            # 期权类型
        unknown_param = 0.00                               # 未知参数
        option_price = round(random.uniform(0.5, 20), 18)  # 期权价格

        row = [
            current_price,
            strike_price,
            volatility,
            dividend_yield,
            risk_free_rate,
            time_to_maturity,
            option_type,
            unknown_param,
            option_price
        ]
        data.append(row)
    return data

# 保存数据到CSV文件
def save_to_csv(data, filename, num_rows):
    header = [
        '當前股價',
        'Strike Price',
        'Volatility',
        'Dividend Yield',
        'Risk Free Rate',
        'Time to Maturity',
        'Option Type',
        'Unknown Param',
        'Option Price'
        ]
    with open(filename, mode='w') as file:
        file.write(str(num_rows) + '\n')
        for row in data:
            file.write(' '.join(map(str, row)) + '\n')


import os
os.makedirs("input", exist_ok=True)


# 生成并保存数据
num_files = 100
for i in range(num_files):
    num_rows = 4
    filename = 'input/parsec_option_data_{}.csv'.format(i)
    option_data = generate_option_data(num_rows)
    save_to_csv(option_data, filename, num_rows)