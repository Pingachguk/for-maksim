import pandas as pd
import requests
from datetime import datetime

df = pd.read_excel("data.xlsx")
if not "Путь к фото" in df.columns:
    df["Путь к фото"] = "-"

session = requests.Session()
adapter = requests.adapters.HTTPAdapter(
    pool_connections=100,
    pool_maxsize=100)
session.mount('http://', adapter)
session.mount('https://', adapter)
session.verify = False
session.headers["Connection"] = "keep-alive"
session.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 YaBrowser/21.8.3.767 (beta) Yowser/2.5 Safari/537.36"
session.verify = False

count = 0
i = 1
for index, item in df.iterrows():
    massiv_photo = item["Ссылка на фото"].split(" | ")
    result = ""
    print(f"На очереди {massiv_photo}")
    if massiv_photo[-1] == "" and len(massiv_photo) >= 2:
        massiv_photo.pop(-1)
        j = 1
        for url in massiv_photo:
            photo = massiv_photo[0]
            filetype = photo.split(".")[-1]
            begin = datetime.now().timestamp()
            content = session.get(photo).content
            name = f"photo/{i}_{j}.{filetype}"
            f = open(f"{name}", "wb")
            f.write(content)
            f.close()
            end = datetime.now().timestamp()
            result = result + name + " | "
            j += 1
        print("[*] Duration: %.2f" % (end - begin))
    elif massiv_photo[0] == "-" and len(massiv_photo) == 1:
        massiv_photo[0] = "-"
        result = massiv_photo[0]
    elif len(massiv_photo) == 1 and not massiv_photo[0] == "":
        photo = massiv_photo[0]
        filetype = photo.split(".")[-1]
        begin = datetime.now().timestamp()
        content = session.get(photo).content
        name = f"photo/{i}.{filetype}"
        f = open(f"{name}", "wb")
        f.write(content)
        f.close()
        end = datetime.now().timestamp()
        print("[*] Duration: %.2f" % (end - begin))
        i += 1
        result = name
    df.loc[index, "Ссылка на фото"] = result
    count += 1
    if count == 100:
        df.to_excel("data_with_photo.xlsx", engine='xlsxwriter', index=False)
        count = 0


# images = [
#     "https://shop.almawin.de/thumbnail/f9/42/3e/1626359774/almawin-4019555705366-2119616_400x400.jpg | ",
#     "https://shop.almawin.de/thumbnail/f9/42/3e/1626359774/almawin-4019555705366-2119616_400x400.jpg", 
#     "https://shop.almawin.de/thumbnail/f2/da/e4/1624915177/almawin-4019555705441-2117923_400x400.jpg | https://shop.almawin.de/thumbnail/f2/da/e4/1624915177/almawin-4019555705441-2117923_400x400.jpg | "
# ]

# i = 1
# for img in images:
#     result = ""
#     massiv_photo = img.split(" | ")
#     if massiv_photo[-1] == "" and len(massiv_photo) >= 2:
#         massiv_photo.pop(-1)
#         j = 1
#         for url in massiv_photo:
#             photo = massiv_photo[0]
#             filetype = photo.split(".")[-1]
#             begin = datetime.now().timestamp()
#             content = requests.get(photo).content
#             f = open(f"photo/{i}_{j}.{filetype}", "wb")
#             f.write(content)
#             f.close()
#             end = datetime.now().timestamp()
#             print("[*] Duration: %.2f" % (end - begin))
#             j += 1
#     elif massiv_photo[0] == "" and len(massiv_photo) == 1:
#         massiv_photo[0] = "-"
#     elif len(massiv_photo) == 1 and not massiv_photo[0] == "":
#         photo = massiv_photo[0]
#         filetype = photo.split(".")[-1]
#         begin = datetime.now().timestamp()
#         content = requests.get(photo).content
#         f = open(f"photo/{i}.{filetype}", "wb")
#         f.write(content)
#         f.close()
#         end = datetime.now().timestamp()
#         print("[*] Duration: %.2f" % (end - begin))
#         i += 1
