import os, sys
import pandas as pd

sumup = 0
for files in os.listdir('reg.energyrating'):
    print(files)

    df = pd.read_csv('reg.energyrating/'+files)
    print(len(df))
    sumup+=len(df)

print(sumup)