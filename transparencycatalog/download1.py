import os
import pandas as pd

df = pd.read_csv("transparencycatalog.csv")

df['EP-PROGRAM URL'] = df['EP-PROGRAM URL'].astype(str)
df['MI-PROGRAM URL'] = df['MI-PROGRAM URL'].astype(str)

pdf1 = df['EP-PROGRAM URL'].values.tolist()
pdf2 = df['MI-PROGRAM URL'].values.tolist()

_pdf1 = [i for i in pdf1 if ".pdf" in i]
_pdf2 = [i for i in pdf2 if ".pdf" in i]

pdfs = _pdf1 + _pdf2

for index, url in enumerate(set(pdfs)):
        try:
            out_image = "PDF/"+ url.split("/")[-1]
            print()
            print(index,"----",out_image,"----",url)
            print()
            os.system("wget -O {0} {1}".format(out_image, url))
        except Exception as e:
            print("Er")