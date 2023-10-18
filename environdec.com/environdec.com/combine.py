import pandas as pd

# df1 = pd.read_csv("level_ecomedes.csv", encoding = "ISO-8859-1")


# # Dropping the rows having NaN/NaT values
# # when threshold of nan values is 2
# df1 = df1.dropna(thresh=5)
 
# # Resetting the indices using df.reset_index()
# df1 = df1.reset_index(drop=True)


# print(df1)


# df2 = pd.read_csv("level_ecomedes_3.csv", encoding = "ISO-8859-1")

# print(df2)

# df3 = pd.read_csv("level_ecomedes_2.csv", encoding = "ISO-8859-1")

# # Dropping the rows having NaN/NaT values
# # when threshold of nan values is 2
# df3 = df3.dropna(thresh=5)
 
# # Resetting the indices using df.reset_index()
# df3 = df3.reset_index(drop=True)

# print(df3)

# df4 = df2.append(df3, ignore_index=True)

# df = df1.append(df4, ignore_index=True)

# print(df)

# df.to_csv('level_ecomedes_merge.csv')

df = pd.read_csv('level_ecomedes_merge.csv')

df['Product Description'] = df['Product Description'].apply(lambda x: str(x).replace('+ Read more', ''))

df.to_csv('level_ecomedes_merge_clean.csv')