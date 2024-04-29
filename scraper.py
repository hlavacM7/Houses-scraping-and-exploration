import pandas as pd
import requests
from bs4 import BeautifulSoup

buy = []
building = []
rooms = []
kitchen = []
square = []
price = []
street = []
area = []

def get_soup(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    return soup

## funkce, která mi vrátí způsob koupě: pronájem/byt, typ bydlení: byt/dům, počet pokoju, typ kuchyně: k/1, rozměry
def get_basics(soup, buy, building, rooms, kitchen, square):
    h2s = soup.find_all("h2", class_="c-products__title")

    for i in range(len(h2s)):
        new = h2s[i].text.replace("\n", " ").replace("\t", "").replace("\xa0", " ").strip().split()
        if "+" in new[2] and "m²" in new:
            buy.append(new[0])
            building.append(new[1])
            square.append(new[3])
            rooms.append(new[2][0])
            kitchen.append(new[2][2])
        else:
            buy.append(0)
            building.append(0)
            square.append(0)
            rooms.append(0)
            kitchen.append(0)

    return buy, building, rooms, kitchen, square

## funkce pro získání ceny
def get_price(soup, price):
    prices = soup.find_all("p", class_= "c-products__price")
    for i in range(len(prices)):
        splitted = prices[i]
        text = splitted.text
        number = ""
        letter = ""
        j = 0
        if "Kč" in text:
            while letter != "K":
                letter = text[j]
                if letter >= '0' and letter <= '9':
                    number += text[j]
                j += 1
            price.append(int(number))
        else:
            price.append(0)

    return price

## funkce pro získání ulice
def get_street(soup, street, area, j):
    streets = soup.find_all ("p", class_ = "c-products__info")

    for i in range(len(streets)):
        new = streets[i].text.replace("\n", " ").replace("\t", "").replace("\xa0", " ").strip()
        street.append(new)
        area.append(j)

    return street

## funkce, která projede všechny stránky pomocí tlačítka další
def get_more(soup):
    link = soup.find("a", class_= "btn paging__item next")
    if link:
        return ("https://reality.idnes.cz" + link.get("href"))
    else:
        return 

urls = [
    "https://reality.idnes.cz/s/prodej/byty/praha/",
    "https://reality.idnes.cz/s/prodej/byty/stredocesky-kraj/",
    "https://reality.idnes.cz/s/prodej/byty/jihocesky-kraj/",
    "https://reality.idnes.cz/s/prodej/byty/plzensky-kraj/",
    "https://reality.idnes.cz/s/prodej/byty/karlovarsky-kraj/",
    "https://reality.idnes.cz/s/prodej/byty/ustecky-kraj/",
    "https://reality.idnes.cz/s/prodej/byty/liberecky-kraj/",
    "https://reality.idnes.cz/s/prodej/byty/kralovehradecky-kraj/",
    "https://reality.idnes.cz/s/prodej/byty/kraj-vysocina/",
    "https://reality.idnes.cz/s/prodej/byty/jihomoravsky-kraj/",
    "https://reality.idnes.cz/s/prodej/byty/zlinsky-kraj/",
    "https://reality.idnes.cz/s/prodej/byty/olomoucky-kraj/",
    "https://reality.idnes.cz/s/prodej/byty/moravskoslezsky-kraj/",
    "https://reality.idnes.cz/s/prodej/byty/pardubicky-kraj/"
]

j = 1

for url in urls:
    while True:
        soup = get_soup(url)
        buy, building, rooms, kitchen, square = get_basics(soup, buy, building, rooms, kitchen, square)
        price = get_price(soup, price)
        street = get_street(soup, street, area, j)
        link = get_more(soup)
        print(len(price))

        if not link:
            break

        url = link
    j += 1

houses = pd.DataFrame(
    {
        "Způsob_koupě": buy,
        "Typ_obydlení": building,
        "Počet_pokojů": rooms,
        "Typ_kuchyně": kitchen,
        "Velikost_bytu": square,
        "Cena": price,
        "Ulice": street,
        "Kraj": area

        
    }
)

houses.to_csv("byty_na_koupi.csv", index = False)
