import json
import time
import requests
from bs4 import BeautifulSoup
import datetime
import csv


# start_time = time.time()


def get_data():
    # cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
    #
    # with open(f"labirint_{cur_time}.csv", "w") as file:
    #     writer = csv.writer(file)

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.120 Safari/537.36"
    }

    url = "https://www.yakaboo.ua/ua/knigi/komp-juternaja-literatura.html"

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    pages_count = int(soup.find("div", class_="yb-pagination__nav-list").find_all("a")[-1].text)
    for i in range(1, pages_count + 1):
        url = f"https://www.yakaboo.ua/ua/knigi/komp-juternaja-literatura.html?p={i}"
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.content, 'lxml')

        items = soup.find_all('div', class_='category-card__content')
        for item in items:
            name = item.find('a', class_='category-card__name').text.strip()
            author = item.find('span', class_='creator-label').text.strip()
            price = item.find('div', class_='ui-price-display__main').find('span').text.strip()
            print(name)
            print(author)
            print(price)



get_data()
