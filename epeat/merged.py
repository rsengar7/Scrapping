import os
import pandas as pd

columns = [
    "Id",
    "Product Name",
    "Product Type",
    "Status",
    "Registered In",
    "Manufacturer",
    "Total Score",
    "EPEAT Tier",
    "Registered On",
    "Archived On",
    "Exceptions",
    "Manufacturer Part Number(s)"
]

column = ",".join(columns)
files = open("epeat_net.csv", "a")
files.write(column)
files.write("\n")
for _dir in os.listdir("files"):
    print(_dir)
    f = open("files/"+_dir, "r")
    _data = f.read()
    # print(_data)
    for row in _data.split("\n")[1:]:
        print("*"*50)
        print(row)
        print("*"*50)
        files.write(row)
        files.write("\n")
    # break
    
