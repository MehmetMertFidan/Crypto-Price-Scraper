import csv
import requests
import pandas as pd
from bs4 import BeautifulSoup

URL='https://coinmarketcap.com/'
data=[]

for page in range(1,6):

    if page > 1:
        new_URL=URL+"?page="+str(page)
    else:
        new_URL=URL

    site=requests.get(new_URL)
    content = BeautifulSoup(site.content , 'html.parser')
    table=content.find("table", class_="sc-936354b2-3 tLXcG cmc-table")
    cryptos=table.find_all("tr")

    for crypto in cryptos:
        symbol=crypto.find("p",class_="coin-item-name")
        price=crypto.find("div",class_="sc-b3fc6b7-0 dzgUIj")
        if symbol:
            if price:
                print(symbol.get_text()+" fiyatı: "+price.get_text())
                data.append([symbol.get_text(), price.get_text()])
        else:
            spans=crypto.find_all("span")
            for span in spans:
                coulmn=crypto.find_all("td")
                if len(coulmn) > 3:
                    fourth_coulmn=coulmn[3]
                    if span:
                        if not span.get("id") and not span.get("class"):
                            print(span.get_text()+ " fiyatı: "+ fourth_coulmn.get_text())
                            data.append([span.get_text(), fourth_coulmn.get_text()])

def save_excel(data):

    df = pd.DataFrame(data, columns=["coin", "price"])
    df.to_excel("crypto_data.xlsx", index=False)

def save_csv(data):

    with open('crypto_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(["coin", "price"])
        writer.writerows(data)

save_excel(data)
save_csv(data)