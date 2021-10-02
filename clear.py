import pandas as pd
import re


def clear():
    file = "data.xlsx"
    data = pd.read_excel(file)

    columns = [
        "Наименование товара",
        "Брэнд",
        "Категория",
        "Серия",
        "Артикул",
        "Цена",
        "Описание",
        "Состав",
        "Объем",
        "Фото",
        "Дополнительная информация",
        "Ссылка",
        "Ссылка на фото"
    ]

    for index, item in data.iterrows():
        for col in columns:
            data.loc[index, col] = re.sub(r"(_x000D_)", " ", str(item[col]))
            data.loc[index, col] = re.sub(r" +", " ", str(item[col]))
            data.loc[index, col] = re.sub(r"\t+", "", str(item[col]))
            data.loc[index, col] = re.sub(r"\n+", "", str(item[col]))
            data.loc[index, col] = re.sub(r"(Produktnummer:)", "", str(item[col]))
            data.loc[index, col] = re.sub(r"(nan)", "-", str(item[col]))
    data.to_excel("data.xlsx", engine='xlsxwriter', index=False)


if __name__ == "__main__":
    clear()
