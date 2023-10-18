import pandas as pd

df = pd.read_csv('euipo_data.csv')
df1 = pd.read_csv('euipo_data_1.csv')
df2 = pd.read_csv('euipo_data_2.csv')
df3 = pd.read_csv('euipo_data_3.csv')
df4 = pd.read_csv('euipo_data_4.csv')
df5 = pd.read_csv('euipo_data_5.csv')
df6 = pd.read_csv('euipo_data_6.csv')
df7 = pd.read_csv('euipo_data_7.csv')
df8 = pd.read_csv('euipo_data_8.csv')
df9 = pd.read_csv('euipo_data_9.csv')
df10 = pd.read_csv('euipo_data_10.csv')
df11 = pd.read_csv('euipo_data_11.csv')
df12 = pd.read_csv('euipo_data_12.csv')

df13 = df.append(df1, ignore_index = True)
df14 = df13.append(df2, ignore_index = True)
df15 = df14.append(df3, ignore_index = True)
df16 = df15.append(df4, ignore_index = True)
df17 = df16.append(df5, ignore_index = True)
df18 = df17.append(df6, ignore_index = True)
df19 = df18.append(df7, ignore_index = True)
df20 = df19.append(df8, ignore_index = True)
df21 = df20.append(df9, ignore_index = True)
df22 = df21.append(df10, ignore_index = True)
df23 = df22.append(df11, ignore_index = True)
df24 = df23.append(df12, ignore_index = True)

print(len(df))
print(len(df1))
print(len(df2))
print(len(df3))
print(len(df4))
print(len(df5))
print(len(df6))
print(len(df7))
print(len(df8))
print(len(df9))
print(len(df10))
print(len(df11))
print(len(df12))

print("--------------")
print(len(df24))

print("---------------")
data = len(df) + len(df1) + len(df2) + len(df3) + len(df4) + len(df5) + len(df6) + len(df7) + len(df8) + len(df9) + len(df10) + len(df11) + len(df12)
print(data)

# df24.to_csv("euipo_data_merge.csv")

# import pandas as pd

# df = pd.read_csv("euipo_data_merge.csv")

df24.drop(['url'], axis=1, inplace=True)

df24['url'] = df24['Filing number'].apply(lambda x: "https://euipo.europa.eu/eSearch/#details/trademarks/{}".format(x))

for index, i in enumerate(df24['url']):
    print(index,"---",i,"----",len(df24))


df24.to_csv("euipo_data_complete.csv")