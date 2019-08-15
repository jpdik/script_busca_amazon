# Script de busca de produtos amazon

### Script feito em python que possibilita a obtenção de informações sobre produtos.

## Instalando dependências

```sh
$ pip install -r requirements.txt
```

## Rodando o script

Ao rodar o comando:

```sh
$ python script.py
```

Será solicitado o termo de busca. Exemplo: sapatos

```sh
Informe o termo de pesquisa: sapatos
```

Depois será solicitado o número de páginas que se deseja buscar:

```sh
Informe o número de páginas que quer obter produtos: 50
```

O script executará até que tenha varrido todas as páginas, ou encontrado uma que não tenha mais produtos:

```sh
Varrendo...
Pagina 22/50.
Parou na página 22/50. Nenhnum produto foi encontrado a partir deste ponto
Terminado. Arquivo Gerado!
```

Por fim o script gerará um arquivo chamado `products.csv`, que pode ser aberto usando excel.

#

[João Paulo de Melo](https://www.jpmdik.com.br)