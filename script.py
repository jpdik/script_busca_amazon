# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import sys

#consts
BASE_URL = "https://www.amazon.com.br/"

def getProductName(product):
    return product.find("a", {"class": "a-link-normal a-text-normal"}).span.text

def getProductImage(product):
    return product.find("img", {"class": "s-image"}).get("src")

def getProductLink(product):
    return BASE_URL + product.find("a", {"class": "a-link-normal a-text-normal"}).get("href")

def getProductRatingOf5Stars(product):
    return product.find("span", {"class", "a-icon-alt"}).text.split()[0] if product.find("span", {"class", "a-icon-alt"}) else -1

def getProductPrice(product):
    price = {}
    # pega todos preços
    prices = product.find_all("span", {"class": "a-price"})
    priceDash = len(product.find_all("span", {"class": "a-price-dash"})) > 1
    if len(prices) > 1:
        # Se ouver um traço(dash) o preço é variante (minimo, máximo). Se não houver, é preço com desconto.
        optionPrice1 = "minValue" if priceDash else "discountValue"
        optionPrice2 = "maxValue" if priceDash else "value"

        price[optionPrice1] = prices[0].find("span", {"class": "a-offscreen"}).text
        price[optionPrice2] = prices[1].find("span", {"class": "a-offscreen"}).text
    elif len(prices) == 1:
        price["value"] = prices[0].find("span", {"class": "a-offscreen"}).text
    else:
        # Grátis
        price["value"] = "0.0"
    return price

def getPrices(object_price):
    data = ""
    for i, (key, value) in enumerate(object_price.items()):
        data+="{}={}{}".format(key,value, "|" if len(object_price.items()) < i else "")

    return data

def getInfoProduct(product):
    info_product = {}
    info_product["name"] = getProductName(product)
    info_product["image"] = getProductImage(product)
    info_product["link"] = getProductLink(product)
    info_product["rating_of_5starts"] = getProductRatingOf5Stars(product)
    info_product["price"] = getProductPrice(product)

    return "{};{};{};{};{}".format(info_product["name"].encode('utf-8'), info_product["image"], info_product["link"], info_product["rating_of_5starts"], getPrices(info_product["price"]))

def searchDataFromPage(searchWord, maxPage, filename="products"):
    f = open("{}.csv".format(filename), "w")

    headers_file ="Name;Image;Link;rating_of_5starts;Price\n"
    f.write(headers_file)

    for countPage in range(maxPage):
        sys.stdout.write("\rPagina {}/{}.".format(countPage+1, maxPage))
        sys.stdout.flush()
        search = 's?k={}&page={}'.format(searchWord, countPage)

        headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

        page = requests.get(BASE_URL+search, headers=headers)

        soup = BeautifulSoup(page.content, 'lxml', from_encoding="utf-8")

        # Pega a lista de produtos completa (limitando para que o filtro fique mais simples com o find ou findall do beautifulsoup)
        list_products = soup.find("div", {"class": "s-result-list s-search-results sg-row"})

        products = list_products.find_all("div", {"class": "s-result-item"})

        if len(products) <= 0:
            print("\nParou na página {}/{}. Nenhnum produto foi encontrado a partir deste ponto".format(countPage+1, maxPage))
            break

        for product in products:
            data = getInfoProduct(product)
            f.write(data+"\n")

    f.close()

if __name__ == "__main__":
    searchWord = raw_input("Informe o termo de pesquisa: ")

    num_pages = ''
    while True:
        try:
            num_pages = int(raw_input("Informe o número de páginas que quer obter produtos: "))
            break
        except (ValueError) as e:
            print("Informe um número válido.")

    print("Varrendo...")
    searchDataFromPage(searchWord, num_pages)
    print("Terminado. Arquivo Gerado!")