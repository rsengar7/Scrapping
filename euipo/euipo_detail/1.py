import pandas as pd

df = pd.read_csv('id.csv')

print(df.head())
print(len(df))

df1 = df[0:200000]
df2 = df[200000:400000]
df3 = df[400000:600000]
df4 = df[600000:800000]
df5 = df[800000:1000000]
df6 = df[1000000:1200000]
df7 = df[1200000:1400000]
df8 = df[1400000:1600000]
df9 = df[1600000:1800000]

print(len(df1))
print(len(df2))
print(len(df3))
print(len(df4))
print(len(df5))
print(len(df6))
print(len(df7))
print(len(df8))
print(len(df9))

df1.reset_index(drop=True, inplace=True)
print(df1.head())

df1.to_csv('id1.csv', index=False)
df2.to_csv('id2.csv', index=False)
df3.to_csv('id3.csv', index=False)
df4.to_csv('id4.csv', index=False)
df5.to_csv('id5.csv', index=False)
df6.to_csv('id6.csv', index=False)
df7.to_csv('id7.csv', index=False)
df8.to_csv('id8.csv', index=False)
df9.to_csv('id9.csv', index=False)