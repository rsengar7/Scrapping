import pandas as pd
import os

# col = "Index,Product Name,Description,About,Features & Specs,Shopping links"
# files = open("consumer_report.csv", "a")
# files.write(col)
# files.write("\n")
# # df = pd.DataFrame()
# for i in os.listdir("consumer_reports_scrap"):
#     print("I------------->",i)

#     f = open("consumer_reports_scrap/"+i, "r")
#     _data = f.read()
#     # print(_data)
#     for j in _data.split("\n")[1:]:
#         print(j)
#         files.write(j)
#         files.write("\n")
#         print("*"*50)
#     # break

df = pd.read_csv("consumer_report.csv")

df = df.dropna()

df.to_csv("consumer_reports_output.csv")