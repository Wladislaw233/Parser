import requests
import sqlite3
from bs4 import BeautifulSoup
import re

HOST = 'https://enter.online/ru/'
URL = 'https://enter.online/ru/komponenty-sistemnyh-pk/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 OPR/79.0.4143.73'
}
def get_html(url, params=''):
    r = requests.get(url, headers = HEADERS, params=params)
    return r
def get_url(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_='tm-category-block uk-box-shadow-hover-large')
    urls = []
    for item in items:
        link = item.get('href')
        urls.append(link)
    return urls

html = get_html(URL)
urls = get_url(html.text)

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='pm-grid-item')
    processors =[]
    for item in items:

        title = item.find('div', class_='ty-grid-list__item-name product-title').get_text(strip=True)

        link_product = item.find('a').get('href')

        price = item.find('span', class_='ty-price').get_text(strip=True)
        remov = ["лей", " "]
        for word in remov:
            price = price.replace(word, "")
        price = int(price)

        res = requests.get(link_product)
        ht2 = res.text
        sp = BeautifulSoup(ht2,"html.parser")
        p = sp.find("table",{"class":"uk-table uk-table-striped tm-attar-table"}).find_all("tr")
        qs = []
        for pr in p:
            txt = pr.get_text(strip=True)
            qs.append(txt)
        qs.pop(0)
        proiz = dict(i.split(':') for i in qs)
        for key in proiz:
            if key == 'Бренд':
                brand = proiz[key]

        link_photo = sp.find("img",{"class":"ty-pict cm-image"}).get("src")

        desc = sp.find("div",{"class":"ty-product-block__note"}).find_next("table").find_all("tr")
        des = []
        for s in desc:
            text = s.get_text(strip=True)
            des.append(text)
        des = list(filter(None, des))
        description = '; '.join(des)

        print(description)
        print(price)
        print(brand)
        print(title)
        processors.append((title,brand,price,description,link_photo,link_product))
    return processors
def parser(urls):
    print(urls)
    processors = []
    for url in urls:
        if (url == urls[0]): PAGENATION = 6
        if (url == urls[1]): PAGENATION = 6
        if (url == urls[2]): PAGENATION = 10
        if (url == urls[3]): PAGENATION = 10
        if (url == urls[4]): PAGENATION = 8
        if (url == urls[5]): PAGENATION = 10
        if (url == urls[6]): PAGENATION = 4
        if (url == urls[7]): PAGENATION = 8
        print(url)
        html = get_html(url)
        if html.status_code == 200:
            for page in range(1, PAGENATION):
                print(f'Parse page {page}')
                html = get_html(url, params={'page': page})
                processors.extend(get_content(html.text))
            print(processors)
        pass
    return processors
processors = parser(urls)
conn = sqlite3.connect("inter.db")
cursor = conn.cursor()
cursor.executemany('INSERT INTO Components VALUES (?,?,?,?,?,?)', processors)
conn.commit()
conn.close()

