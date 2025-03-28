import pandas as pd

file_path = "1975.csv"
df = pd.read_csv(file_path)
print(df.columns)
print(df)