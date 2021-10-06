import pandas as pd
import requests

df = pd.read_excel("data.xlsx")

for data in df.values():
    print()

# for img in images:
#     if img == "":
#         continue
#     filetype = img.split(".")[-1]
#     content = requests.get(img).content
#     f = open(f"photo/1.{filetype}", "wb")
#     f.write(content)
#     f.close()

