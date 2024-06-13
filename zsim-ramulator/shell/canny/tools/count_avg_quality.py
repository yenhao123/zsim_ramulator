import pandas as pd

file = "/root/ramulator-pim/zsim-ramulator/shell/canny/quality/quality.csv"
df = pd.read_csv(file)
df.columns = ["row", "quality"]
print(df["quality"][1:].mean())
