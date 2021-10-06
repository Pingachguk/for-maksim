import pandas as pd
import requests

try:
    images = "https://biothal.ru/image/catalog/a2a/6.jpg | ".split(" | ")
except:
    images = "https://biothal.ru/image/catalog/a2a/6.jpg"

for img in images:
    if img == "":
        continue
    filetype = img.split(".")[-1]
    content = requests.get(img).content
    f = open(f"photo/1.{filetype}", "wb")
    f.write(content)
    f.close()

