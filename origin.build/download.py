# M, L Certifications. Features

import pandas as pd
import os

df = pd.read_csv("origin.build.csv")

print(df)

cert = df['Certifications']

features = df['Features'].values.tolist()


# print(cert[0])
li = []

for i in cert:
    # print(i)
    try:
        for j in i.split():
            if "https" in j and ".pdf" in j:
                print(j)
                li.append(j.replace("'","").replace(",",""))
    except:
        print("*"*100)
        print(i)
    # break

for i in features:
    try:
        for j in i.split():
            if "https" in j and ".pdf" in j:
                print(j.replace("}",""))
                li.append(j.replace("}","").replace("'","").replace(",",""))
    except:
        print("*"*100)
        print(i)
    # break

# print(features[0])

print(len(li))

li1 = set(li)

print(len(li1))

for index, url in enumerate(li1):
    out_image = "Pdf/"+ url.split("/")[-1]
    print()
    print(index,"----",out_image,"----",url)
    print()
    os.system("wget -O {0} {1}".format(out_image, url))