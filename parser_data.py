import pandas as pd
import requests
import bs4


def get_page(url) -> bs4.BeautifulSoup:
    content = requests.get(url).text
    soup = bs4.BeautifulSoup(content, "html.parser")
    return soup


def get_catalog(page, classname):
    catalog = page.find(class_=classname)
    return catalog


def get_items(catalog, classname):
    items = catalog.find_all(class_=classname)
    return items


def paginator(url, page):
    return get_page(url.format(page))


def get_title(item, classname):
    return item.find(class_=classname).find("a")


def get_img_src(item, classname):
    return item.find(class_=classname).find("img")["src"]


# def set_item():
#     item = {
#         "Наименование товара": name,
#         "Категория": category,
#         "Серия": "",
#         "Артикул": "",
#         "Цена": "",
#         "Описание": "",
#         "Состав": "",
#         "Фото": "",
#         "Дополнительная информация": "",
#         "Ссылка": "",
#         "Ссылка на фото": "",
#     }


def get_ecl_items(data):
    items = []
    uri = "https://ec-l.ru"

    url_dict = {
        "Уход за лицом": "https://ec-l.ru/catalog/ukhod-za-litsom/",
        "Уход за волосами": "https://ec-l.ru/catalog/ukhod-za-volosami/",
        "Уход за телом": "https://ec-l.ru/catalog/ukhod-za-telom/",
        "Мужская серия": "https://ec-l.ru/catalog/muzhskaya-seriya/",
        "Детская серия": "https://ec-l.ru/catalog/detskaya-seriya/",
        "Серия SPA": "https://ec-l.ru/catalog/spa/",
        "Серия 'Страный'": "https://ec-l.ru/catalog/strany/",
        "LovECoil": "https://ec-l.ru/catalog/lovecoil/",
    }
    link_categories = []
    
    for serie, url in url_dict.items():
        content = requests.get(url).text
        soup = bs4.BeautifulSoup(content, "html.parser")
        categories = soup.find(class_="filter-section").find_all("a")
    
        for a in categories:
            link_categories.append({
                "Серия": serie,
                "Категория": a.text,
                "Ссылка": a["href"],
            })

    for category in link_categories:
        # "serie": serie,
        # "name": a.text,
        # "link": a["href"]
        content = requests.get(uri+category['Ссылка']).text
        print(uri+category['Ссылка'])
        soup = bs4.BeautifulSoup(content, "html.parser")

        page_div = soup.find(class_="pagenav")
        
        if not page_div:
            max_page = 1
        else:
            max_page = len(page_div.find_all("a"))

        for i in range(1, max_page+1):
            content = requests.get(uri+category['Ссылка']+f"?page={i}").text
            soup = bs4.BeautifulSoup(content, "html.parser")
            catalog = soup.find(class_="cnt_box").find_all("li")
            for row in catalog:
                item = {
                    "Наименование товара": "",
                    "Категория": "",
                    "Серия": "",
                    "Артикул": "",
                    "Цена": "",
                    "Описание": "",
                    "Состав": "",
                    "Фото": "",
                    "Дополнительная информация": "",
                    "Ссылка": "",
                    "Ссылка на фото": "",
                }

                link = row.find("h3").find("a")
                content = requests.get(uri+link["href"]).text
                soup = bs4.BeautifulSoup(content, "html.parser") 
                info = soup.find(class_="info")
                photo = soup.find(class_="photos").find("img")["src"]
                descr = info.find(class_="tabs").find("div").find_all("div")
                item["Наименование товара"] = link.text
                item["Брэнд"] = "EO Laboratorie"
                item["Категория"] = category['Категория']
                item["Серия"] = category['Серия']
                item["Артикул"] = "-" 
                item["Цена"] = "Узнается у продавца" 
                item["Описание"] = descr[1].text
                item["Состав"] = descr[3].text
                item["Фото"] = photo
                item["Дополнительная информация"] = descr[2].text
                item["Ссылка"] = uri+link["href"]
                item["Ссылка на фото"] = uri+photo
                data = data.append(item, ignore_index=True)
                data.to_excel("data.xlsx", engine='xlsxwriter', index=False)
                items.append(item)

    return data

def get_organic_shop(data):
    items = []
    url = "https://organic-shops.ru/products/?page={}"
    uri = "https://organic-shops.ru"
    
    max_page = 156

    for i in range(0, max_page+1):
        soup = get_page(url.format(i))
        print(url.format(i))

        catalog = soup.find(class_="items").find_all(class_="item")

        for row in catalog:
            item = {
                "Наименование товара": "",
                "Категория": "",
                "Серия": "",
                "Артикул": "",
                "Цена": "",
                "Описание": "",
                "Состав": "",
                "Фото": "",
                "Дополнительная информация": "",
            }
            try:
                link = row.find("a")["href"]
                brand = row.find(class_="brend").text
                name = row.find(class_="name").text
                photo = row.find(class_="firstp")["src"]

                page = get_page(uri+link)

                info = page.find(class_="info")
                articul: str = info.find_all("span")[0].text
                brand_serie: str = info.find_all("span")[1].text

                tabs = page.find(class_="tabsform").find_all(class_="tab-pane")
                descr = page.find(id="oo1").text
                instr = page.find(id="oo2").text
                sostav = page.find(id="oo3").text
                price = page.find(class_="price").find(class_="newprice").text
                item["Фото"] = photo
                item["Категория"] = page.find_all(class_="breadcrumb-item")[-1].text
                item["Наименование товара"] = name
                item["Брэнд"] = brand
                item["Артикул"] = articul.replace("Артикул:", "")
                item["Серия"] = brand_serie.replace("Линия:", "").replace(brand, "")
                item["Описание"] = descr.replace("\n", "")
                item["Состав"] = sostav
                item["Цена"] = price
                item["Дополнительная информация"] = instr
                item["Ссылка"] = uri+link
                item["Ссылка на фото"] = uri+photo
                data = data.append(item, ignore_index=True)
                data.to_excel("data.xlsx", engine='xlsxwriter', index=False)
                items.append(item)
            except:
                pass
    return data

def get_levrana(data):
    items = {}
    url = "https://levrana.ru/catalog/?PAGEN_1={}"
    uri = "https://levrana.ru"
    catalog_class = "catalog_block"
    product_class = "product-item-wrap" # Класс продукта в каталоге
    max_page = 38
    price_class = "price_value" # Перед заходом на страницу товара надо парсить
    img_class = "image_wrapper_block" # Img парсить перед заходом
    name_prod_class = "item-title" # Name
    descr_class = "desc-card-block--text" # Надо извлечь параграфы
    sostav_class = "full-composition-block--text"
    add_info_class = "application-block--text-center"
    articul_class = "product-article-card" # Replace артикул на "" 
    count = 0

    for i in range(1, max_page+1):
        try:
            page = paginator(url, i)
            catalog = get_catalog(page, catalog_class)
            items = get_items(catalog, product_class)
            for prod in items:
                item = {
                    "Наименование товара": "",
                    "Категория": "",
                    "Серия": "",
                    "Артикул": "",
                    "Цена": "",
                    "Описание": "",
                    "Состав": "",
                    "Фото": "",
                    "Дополнительная информация": "",
                    "Ссылка": "",
                    "Ссылка на фото": "",
                }
                title = get_title(prod, name_prod_class)
                name = title.get_text()
                link = uri+title["href"]
                price = prod.find(class_=price_class).text
                photo = prod.find(class_=img_class).find("img")["src"]
                url_photo = uri+photo

                page_item = get_page(link)
                descr = page_item.find(class_=descr_class).text
                sostav = page_item.find(class_=sostav_class).text
                articul = page_item.find(class_=articul_class).text
                add_info = page_item.find(class_=add_info_class).text

                item["Фото"] = photo
                item["Категория"] = "-"
                item["Наименование товара"] = name.replace("\n", "")
                item["Брэнд"] = "Levrana"
                item["Артикул"] = articul.replace("\n", "")
                item["Серия"] = "-"
                item["Описание"] = descr.replace("\n", "")
                item["Состав"] = sostav.replace("\n", "")
                item["Цена"] = price.replace("\n", "")
                item["Дополнительная информация"] = add_info.replace("\n", "")
                item["Ссылка"] = link
                item["Ссылка на фото"] = url_photo
                data = data.append(item, ignore_index=True)
                data.to_excel("data.xlsx", engine='xlsxwriter', index=False)
                count += 1
                print(f"[+] Add {count}")
        except Exception as e:
            print(e)

    return data


def get_miko(data):
    uri = "https://www.mi-ko.org"
    categories = {
        "ДЛЯ ЛИЦА": "https://www.mi-ko.org/catalog/dlya_litsa/?SHOWALL_1=1",
        "ДЛЯ ТЕЛА": "https://www.mi-ko.org/catalog/dlya_tela/?SHOWALL_1=1",
        "ДЛЯ ВОЛОС": "https://www.mi-ko.org/catalog/dlya_volos/?SHOWALL_1=1",
        "ДЛЯ МУЖЧИН": "https://www.mi-ko.org/catalog/dlya_muzhchin/?SHOWALL_1=1",
        "ДЛЯ ДЕТЕЙ": "https://www.mi-ko.org/catalog/dlya_detey/?SHOWALL_1=1",
        "МАСЛА": "https://www.mi-ko.org/catalog/masla_2/?SHOWALL_1=1",
        "БЫТОВАЯ НЕХИМИЯ": "https://www.mi-ko.org/catalog/bytovaya_nekhimiya/?SHOWALL_1=1",
    }

    count = 0

    catalog_classname = "catalog__main"
    product_classname = "catalog__main__product"
    price_classname = "catalog__main__product__price"
    title_classname = "catalog__main__product__name"
    sostav_classname = "product-card__main__product-info__sub"
    descr_classname = "indtabs__content" # First indtabs
    img_classname = "product-card__accomp__inner__card__img" # Get img and their src
    product_link_classname = "catalog__main__product_link"
    category_classname = "bx-breadcrumb-item" # Find all <li> and get -2 item
    articul_classname = "-"

    for name_url, catalog_url in categories.items():
        page = get_page(catalog_url)
        catalog = get_catalog(page, catalog_classname)
        items = get_items(catalog, product_classname)
        for product in items:
            try:
                link = product.find("a", class_=product_link_classname)["href"]
                page_product = get_page(uri+link)
                item = {
                    "Брэнд": "miko",
                    "Наименование товара": product.find(class_=title_classname).text.replace('\n', ''),
                    "Категория": page_product.find_all(class_=category_classname)[-2].text.replace('\n', ''),
                    "Серия": "-",
                    "Артикул": "-",
                    "Цена": product.find(class_=price_classname).text.replace('\n', ''),
                    "Описание": page_product.find_all(class_=descr_classname)[0].text.replace('\n', ''),
                    "Состав": page_product.find(class_=sostav_classname).text.replace('\n', ''),
                    "Фото": product.find(class_=img_classname).find("img")["src"],
                    "Дополнительная информация": page_product.find_all(class_=descr_classname)[2].text.replace('\n', ''),
                    "Ссылка": uri+link,
                    "Ссылка на фото": uri+product.find(class_=img_classname).find("img")["src"],
                }
                count += 1
                print(f"[+] Add {count}")
                data = data.append(item, ignore_index=True)
                data.to_excel("data.xlsx", engine='xlsxwriter', index=False)
            except Exception as e:
                print(e)
    return data


def get_craft_cosmetic(data):
    count = 0
    max_page = 18
    url = "https://craft-cosmetics.ru/production?page={}"
    uri = "https://craft-cosmetics.ru"

    catalog_classname = "view-content"
    name_classname = "title_node"
    title_classname = "views-field-title"
    product_classname = "views-row"
    price_classname = "views-field-field-ingredients-price"
    img_classname = "field-name-field-production-img" # On product page
    sostav_classname = "field-name-field-production-components"
    add_info_classname = "field-name-field-ingredients-use"
    descr_classname = "field-name-body"
    category_classname = "page_title" 

    for i in range(max_page):
        page = get_page(url.format(i))
        catalog = get_catalog(page, catalog_classname)
        items = get_items(catalog, product_classname)
        for product in items:
            try:
                link = product.find(class_ =title_classname).find("a")["href"]
                page_product = get_page(uri+link)

                category = page_product.find_all(class_=category_classname)

                if len(category):
                    category = category[0].text
                else:
                    category = "-" 

                item = {
                    "Брэнд": "miko",
                    "Наименование товара": page_product.find(class_=name_classname).text.replace('\n', ''),
                    "Категория": category,
                    "Серия": "-",
                    "Артикул": "-",
                    "Цена": product.find(class_=price_classname).text.replace('\n', ''),
                    "Описание": page_product.find(class_=descr_classname).text.replace('\n', ''),
                    "Состав": page_product.find(class_=sostav_classname).text.replace('\n', ''),
                    "Фото": page_product.find(class_=img_classname).find("img")["src"],
                    "Дополнительная информация": page_product.find(class_=add_info_classname).text.replace('\n', ''),
                    "Ссылка": uri+link,
                    "Ссылка на фото": page_product.find(class_=img_classname).find("img")["src"],
                }
                count += 1
                print(f"[+] Add {count}")
                data = data.append(item, ignore_index=True)
                data.to_excel("data.xlsx", engine='xlsxwriter', index=False)
            except Exception as e:
                print(e)
    return data


def get_organic_zone(data):
    count = 0
    url = "https://organic-zone.ru/production?page={}"
    uri = "https://organic-zone.ru"
    max_page = 48

    catalog_classname = "view-content"
    product_classname = "views-row"
    price_classname = "views-field-field-ingredients-price"
    name_classname = "sec_title" # Find all and get [1]
    category_classname = "sec_title" # Find all and get [0]
    title_classname = "views-field-title"
    img_classname = "field-name-field-production-img" # On product page
    sostav_classname = "field-name-field-production-components"
    add_info_classname = "field-name-field-ingredients-use"
    descr_classname = "field-name-body"

    for i in range(max_page):
        # print(url.format(i))
        page = get_page(url.format(i))
        catalog = get_catalog(page, catalog_classname)
        items = get_items(catalog, product_classname)
        for product in items:
            try:
                link = product.find(class_ =title_classname).find("a")["href"]
                page_product = get_page(link)

                category = page_product.find_all(class_=category_classname)

                if len(category):
                    category = category[0].text.replace("\n", "")
                else:
                    category = "-" 

                # page_product.find_all(class_=name_classname)[1].text.replace('\n', '')

                item = {
                    "Брэнд": "OrganicZone",
                    "Наименование товара": product.find(class_=title_classname).text,
                    "Категория": category,
                    "Серия": "-",
                    "Артикул": "-",
                    "Цена": product.find(class_=price_classname).text.replace('\n', ''),
                    "Описание": page_product.find(class_=descr_classname).text.replace('\n', ''),
                    "Состав": page_product.find(class_=sostav_classname).text.replace('\n', ''),
                    "Фото": page_product.find(class_=img_classname).find("img")["src"],
                    "Дополнительная информация": page_product.find(class_=add_info_classname).text.replace('\n', ''),
                    "Ссылка": uri+link,
                    "Ссылка на фото": page_product.find(class_=img_classname).find("img")["src"],
                }
                count += 1
                print(f"[+] Add {count}")
                data = data.append(item, ignore_index=True)
                data.to_excel("data.xlsx", engine='xlsxwriter', index=False)
            except Exception as e:
                print(e)
    return data


def get_innature(data):
    uri = "https://in-nature.ru"
    count = 0
    categories = {
        "Для лица": "https://in-nature.ru/catalog/dlya-lica?page={}",
        "Для тела": "https://in-nature.ru/catalog/dlya-tela?page={}",
        "Для волос": "https://in-nature.ru/catalog/dlya-volos?page={}",
        "Серия INNATURE AQUA": "https://in-nature.ru/catalog/seriya-innature-aqua?page={}",
        "Серия INNATURE SHINE": "https://in-nature.ru/catalog/seriya-innature-shine?page={}",
    }

    catalog_classname = "view-content"
    product_classname = "views-row"
    price_classname = "views-field-field-ingredients-price"
    name_classname = "sec_title" # Find all and get [1]
    category_classname = "main_breadcrumbs" # Find all and get [-1]
    title_classname = "views-field-title"
    img_classname = "views-field-field-production-img" # On product page
    sostav_classname = "field-name-field-production-components"
    add_info_classname = "field-name-field-ingredients-use"
    descr_classname = "field-name-body"

    for cat, url in categories.items():
        for i in range(5):
            page = paginator(url, i)
            empty = page.find(class_="view-empty")
            if empty:
                break
            # catalog = get_catalog(page, catalog_classname)
            catalog = page.find_all(class_=catalog_classname)[1]
            items = get_items(catalog, product_classname)


            for product in items:
                page_product = get_page(uri+product.find(class_=title_classname).find("a")["href"])
                category: str = page_product.find(class_=category_classname).find_all("span")[-2].text

                if category.rfind("Серия") == -1:
                    serie = "-"
                else:
                    serie = category.replace("Серия", "")

                item = {
                    "Брэнд": "INNATURE",
                    "Наименование товара": product.find(class_=title_classname).text,
                    "Категория": cat+"/"+category,
                    "Серия": serie,
                    "Артикул": "-",
                    "Цена": product.find(class_=price_classname).text.replace('\n', ''),
                    "Описание": page_product.find(class_=descr_classname).text.replace('\n', ''),
                    "Состав": page_product.find(class_=sostav_classname).text.replace('\n', ''),
                    "Фото": product.find(class_=img_classname).find("img")["src"],
                    "Дополнительная информация": page_product.find(class_=add_info_classname).text.replace('\n', ''),
                    "Ссылка": uri+product.find(class_=title_classname).find("a")["href"],
                    "Ссылка на фото": product.find(class_=img_classname).find("img")["src"],
                }
                count += 1
                print(f"[+] Add {count}")
                data = data.append(item, ignore_index=True)
                data.to_excel("data.xlsx", engine='xlsxwriter', index=False)
    return data


def get_biothal(data):
    count = 0
    uri = "https://biothal.ru"

    categories = {
        "Для лица": "https://biothal.ru/lico",
        "Для тела": "https://biothal.ru/telo",
        "Эффективные наборы": "https://biothal.ru/nabory",
    }

    catalog_classname = "container"
    subcatalog_classname = "box-with-products"
    category_classname = "box-heading"
    items_classname = "product"
    title_classname = "prod_link"
    price_classname = "price"
    img_classname = "image"
    img_classname2 = "product-image"
    descr_id = "tab-description"
    sostav_id = "tab-apt0"
    addinfo_id = "tab-apt1"

    for cat, url in categories.items():
        page = get_page(url)
        catalogs = page.find_all(class_=subcatalog_classname)
        
        for catalog in catalogs:
            category = catalog.find(class_=category_classname).text
            items = catalog.find_all(class_=items_classname)

            for item in items:
                url = item.find(class_=img_classname).find("a")["href"]
                page_product = get_page(url)
                product = {
                    "Брэнд": "BIOTHAL",
                    "Наименование товара": item.find(class_=title_classname).text,
                    "Категория": cat+"/"+category,
                    "Серия": "-",
                    "Артикул": "-",
                    "Цена": item.find(class_=price_classname).find_all("span")[0].text.replace('\n', ''),
                    "Описание": page_product.find(id=descr_id).text.replace('\n', ''),
                    "Состав": page_product.find(id=sostav_id).text.replace('\n', ''),
                    "Фото": get_img_src(page_product, img_classname2),
                    "Дополнительная информация": page_product.find(id=addinfo_id).text.replace('\n', ''),
                    "Ссылка": url,
                    "Ссылка на фото": uri+get_img_src(page_product, img_classname2),
                }
                count += 1
                print(f"[+] Add {count}")
                data = data.append(product, ignore_index=True)
                data.to_excel("data.xlsx", engine='xlsxwriter', index=False)
    return data


def get_dnc(data):
    count = 0
    uri = "https://dncbrand.ru"
    url_catalog = "https://dncbrand.ru/catalog?page={}"
    max_page = 15 # [1, 15]

    catalog_classname = "products-wrapper"
    items_classname = "c-goods__trigger"
    price_classname = "c-goods__price--current"
    title_classname = "c-goods__title"
    img_classname = "c-goods__img"
    info_classname = "c-tab__content--active"
    articul_classname = "label-article" # get span
    category_itemprop = "itemListElement"
    category_classname = "bread-crumbs__item"

    for i in range(1, max_page):
        try:
            page = paginator(url_catalog, i)
            catalog = get_catalog(page, catalog_classname)
            items = get_items(catalog, items_classname)

            for item in items:
                url = item.find(class_=title_classname)["href"]
                page_product = get_page(url)

                info = page_product.find(class_=info_classname).text.replace('\n', '')
                sostav = info[info.find("Состав"):len(info)-1]
                descr = info[0:info.find("Состав")]

                product = {
                    "Брэнд": "DNC",
                    "Наименование товара": item.find(class_=title_classname).text.replace("\n", ""),
                    "Категория": page_product.find_all(class_=category_classname)[-3].text,
                    "Серия": "-",
                    "Артикул": page_product.find(class_=articul_classname).text.replace("\n", ""),
                    "Цена": item.find(class_=price_classname).find_all("span")[0].text.replace('\n', ''),
                    "Описание": descr,
                    "Состав": sostav,
                    "Фото": get_img_src(item, img_classname),
                    "Дополнительная информация": "-",
                    "Ссылка": url,
                    "Ссылка на фото": item.find(class_="c-goods__img").find("img")["src"],
                }
                count += 1
                print(f"[+] Add {count}")
                data = data.append(product, ignore_index=True)
                data.to_excel("data.xlsx", engine='xlsxwriter', index=False)
        except Exception as e:
            print(e)
    return data


def get_klar(data):
    max_page = 3 # [1, 3]
    url = "https://shop.almawin.de/Klar/?order=name-asc&p={}"
    uri = "https://shop.almawin.de/"
    catalog_classname = "js-listing-wrapper"
    items_classname = "product-box"
    price_classname = "product-price"
    img_classname = "product-image-wrapper"
    title_classname = "product-name"
    info_classname = "product-detail-description" # [0] descr [1] add_info [3] sostav 



def start_parser() -> pd.DataFrame:
    print("[*] Start parser")
    columns = [
        "Наименование товара",
        "Брэнд",
        "Категория",
        "Серия",
        "Артикул",
        "Цена",
        "Описание",
        "Состав",
        "Фото",
        "Дополнительная информация",
        "Ссылка",
        "Ссылка на фото"
        ]
    data = pd.DataFrame(columns=columns)

    data = get_ecl_items(data)
    data = get_organic_shop(data)
    data = get_levrana(data)
    data = get_miko(data)
    data = get_craft_cosmetic(data)
    data = get_organic_zone(data)
    data = get_innature(data)
    data = get_biothal(data)
    data = get_dnc(data)

    return data
