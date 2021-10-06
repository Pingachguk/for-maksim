import pandas as pd
import requests
from datetime import datetime

df = pd.read_excel("data.xlsx")

images = [
    "https://shop.almawin.de/thumbnail/f9/42/3e/1626359774/almawin-4019555705366-2119616_400x400.jpg | ",
    "https://shop.almawin.de/thumbnail/f9/42/3e/1626359774/almawin-4019555705366-2119616_400x400.jpg", 
    "https://shop.almawin.de/thumbnail/f2/da/e4/1624915177/almawin-4019555705441-2117923_400x400.jpg | https://shop.almawin.de/thumbnail/f2/da/e4/1624915177/almawin-4019555705441-2117923_400x400.jpg | "
]

i = 1
for img in images:
    massiv_photo = img.split(" | ")
    if massiv_photo[-1] == "" and len(massiv_photo) >= 2:
        massiv_photo.pop(-1)
    elif massiv_photo[0] == "" and len(massiv_photo) == 1:
        massiv_photo[0] = "-"
        continue
    elif True: pass
    print(massiv_photo)
    # photo = data[-1]
    # filetype = photo.split(".")[-1]
    # begin = datetime.now().timestamp()
    # content = requests.get(photo).content
    # f = open(f"photo/{i}.{filetype}", "wb")
    # f.write(content)
    # f.close()
    # end = datetime.now().timestamp()
    # print("[*] Duration: %.2f" % (end - begin))
    # i += 1

# for img in images:
#     if img == "":
#         continue
#     filetype = img.split(".")[-1]
#     content = requests.get(img).content
#     f = open(f"photo/1.{filetype}", "wb")
#     f.write(content)
#     f.close()

