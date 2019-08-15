# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import sys

# constantes
BASE_URL = "https://www.amazon.com.br/"

## obtém o nome do produto.
def getProductName(product):
    return product.find("a", {"class": "a-link-normal a-text-normal"}).span.text

## obtém o link da imagem do produto
def getProductImage(product):
    return product.find("img", {"class": "s-image"}).get("src")

## obtém um link para acesso ao produto (pode ser usado para acessar a página que tem mais informações ainda do produto e continuar varrendo a amazon)
def getProductLink(product):
    return BASE_URL + product.find("a", {"class": "a-link-normal a-text-normal"}).get("href")

## obtém o valor de estrelas que o produto recebeu. Caso não possua uma avaliação retorna -1.
def getProductRatingOf5Stars(product):
    return product.find("span", {"class", "a-icon-alt"}).text.split()[0] if product.find("span", {"class", "a-icon-alt"}) else -1

### analisa os campos dentro do card do produto e retorna somente um objeto com os preços do produto (promoção, variação ou grátis) 
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

## Obtém os preços dentro de um unico campo do csv, formatando o dicionario que foi criado para pura string
def getPrices(object_price):
    data = ""
    for i, (key, value) in enumerate(object_price.items()):
        data+="{}={}{}".format(key,value, "|" if len(object_price.items()) < i else "")

    return data

## Obtem todas as informações de cada produto e formata-os devidamente para o formado csv antes de retornar
def getInfoProduct(product):
    info_product = {}
    info_product["name"] = getProductName(product)
    info_product["image"] = getProductImage(product)
    info_product["link"] = getProductLink(product)
    info_product["rating_of_5starts"] = getProductRatingOf5Stars(product)
    info_product["price"] = getProductPrice(product)

    return "{};{};{};{};{}".format(info_product["name"].encode('utf-8'), info_product["image"], info_product["link"], info_product["rating_of_5starts"], getPrices(info_product["price"]))

## Função principal. ela abre o arquivo, faz a requisição para cada página da amazon quando ela ainda tiver produtos e armazena is dados.
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

        # Obtêm o campos que representam cada card dentro da página da amazon
        products = list_products.find_all("div", {"class": "s-result-item"})

        # se a página não possui nenhum desses cards, ela está vazia.
        if len(products) <= 0:
            print("\nParou na página {}/{}. Nenhnum produto foi encontrado a partir deste ponto".format(countPage+1, maxPage))
            break

        # para cada card de produto, coleta suas informações na variável data já devidamente formatada para csv, e escreve uma nova linha no arquivo
        for product in products:
            data = getInfoProduct(product)
            f.write(data+"\n")

    f.close()

## Main da aplicação
if __name__ == "__main__":
    searchWord = raw_input("Informe o termo de pesquisa: ")

    #Valida o número informado.
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