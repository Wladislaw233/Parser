import requests
import sqlite3
from bs4 import BeautifulSoup
import re

HOST = 'https://enter.online/ru/'
URL = 'https://enter.online/ru/kompyutery/cpu/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 OPR/79.0.4143.73'
}
def get_html(url, params=''):
    r = requests.get(url, headers = HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='pm-grid-item')
    processors =[]
    for item in items:
        title = item.find('div', class_='ty-grid-list__item-name product-title').get_text(strip=True)
        link_product = item.find('a').get('href')
        price = item.find('span', class_='ty-price').get_text(strip=True)
        remov = ["лей"," "]
        for word in remov:
            price = price.replace(word, "")
        res = requests.get(link_product)
        ht2 = res.text
        sp = BeautifulSoup(ht2,"html.parser")
        proiz = sp.find("td",{"class":"uk-width-1-2 tm-text-wrap"}).get_text(strip=True)
        p = title
        p = p.split()
        proiz = p[1]
        link_photo = sp.find("img",{"class":"ty-pict cm-image"}).get("src")
        description = sp.find("div",{"class":"ty-product-block__note"}).find_next("table").get_text(strip=True)
        price = int(price)
        processors.append((title,proiz,price,description,link_photo,link_product))
    return processors

def parser():
    PAGENATION = 6
    html = get_html(URL)
    if html.status_code == 200:
        processors =[]

        for page in range(1, PAGENATION):
            print(f'Parse page {page}')
            html = get_html(URL, params={'page': page})
            processors.extend(get_content(html.text))
        print(processors)
        return processors

        pass
    else:
        print('Error')
        return 0

processors = parser()

conn = sqlite3.connect("inter.db")
cursor = conn.cursor()
cursor.executemany('INSERT INTO Processors VALUES (?,?,?,?,?,?)', processors)
conn.commit()
conn.close()

