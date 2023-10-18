import os
import zipfile

for _zip in os.listdir("Zips"):
    print("Zip---->",_zip)
    with zipfile.ZipFile("Zips/"+_zip,"r") as zip_ref:
        zip_ref.extractall("Pdf")