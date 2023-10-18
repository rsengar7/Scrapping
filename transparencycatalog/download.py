import wget, os
import pandas as pd

df = pd.read_csv("transparencycatalog.csv")

df['EP-PROGRAM URL'] = df['EP-PROGRAM URL'].astype(str)
df['MI-PROGRAM URL'] = df['MI-PROGRAM URL'].astype(str)

pdf1 = df['EP-PROGRAM URL'].values.tolist()
pdf2 = df['MI-PROGRAM URL'].values.tolist()

_pdf1 = [i for i in pdf1 if ".pdf" in i]
_pdf2 = [i for i in pdf2 if ".pdf" in i]

pdfs = set(_pdf1 + _pdf2)

print(len(set(pdfs)))


# index = 0
# for num, url in enumerate(pdfs):
#     print(num,"---",url)
#     if url == 'https://info.nsf.org/Certified/Sustain/ProdCert/EPD10429.pdf':
#         index = 1

#     if index == 1:
#         try:
#             # url = "https://cdn.scscertified.com/products/cert_pdfs/HON_2021_SCS-SCF-05952_s.pdf"
#             wget.download(url, "PDF/"+str(url).split("/")[-1])
#             print()
#             # wget.download(url)
#             # break
#         except Exception as e:
#             print("Error --->",e)
#             # break

    # out_image = "Pdf/"+str(url).split("/")[-1]
    # # url = 'http://mangadoom.co/wp-content/manga/5170/886/005.png'
    # os.system("wget -O {0} {1}".format(out_image, url))
    # # break