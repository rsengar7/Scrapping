import pandas as pd

df = pd.read_csv('declare-living.csv')
df1 = pd.read_csv('declare-living-detail.csv')

df2 = pd.merge(df, df1, on='URL', how='left')
print(df2.head(2))

print(df2.columns)

df3 = df2[['URL', 'Product_x', 'Company_x', 'Declare Id', 'Licence Expiration', 'Lpc Certified', 'Life Expectancy', 'End Of Life Options', 
    'Declared Unit', 'Embodied Carbon', 'Assessor', 'Phone', 'Ingredient List'
]]

df3.rename(columns={'Product_x': 'Product', 'Company_x': 'Company'}, inplace=True)

print(df3.columns)


df3.to_csv('declare-living-future.csv')