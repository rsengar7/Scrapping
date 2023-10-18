import wget
import pandas as pd


df = pd.read_csv('geca_eco.csv')

pdf = df['pdf'].values.tolist()

print(len(pdf))

print(set(pdf))
# for index, url in enumerate(pdf):
#     if url != "":
#         print(index)

#         out_image = "Pdf/"+ str(epd_name)+".pdf"
#         print(out_image)
#         os.system("wget -O {0} {1}".format(out_image, epd_download))