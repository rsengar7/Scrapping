import os, sys, time
import pandas as pd

files = open("sedar.csv", "a")
column = "Company Name,Company URL,Date of Filling,Time of Filling,Document Type,Docuement URL,File Type,File Size"
files.write(column)
files.write("\n")
for _dir in os.listdir("New"):
    time.sleep(2)
    # print(_dir)
    f = open("New/"+_dir, "r")
    _data = f.read()
    # print(_data)
    for row in _data.split("\n")[1:]:
        print("*"*50)
        print(row)
        print("*"*50)
        # sys.exit()
        # break
        files.write(row)
        files.write("\n")