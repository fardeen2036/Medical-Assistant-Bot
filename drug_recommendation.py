import pandas as pd

file_path = r"D:\OneDrive\Desktop\new\dataset\Drug prescription to disease\final.csv"
df = pd.read_csv(file_path)
print(df.columns)  # Log the column names