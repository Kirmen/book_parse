import json
import time
import requests
from bs4 import BeautifulSoup
import datetime
import csv


# start_time = time.time()


def get_data():
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

    with open(f"yakaboo_{cur_time}.csv", "w", encoding='UTF-8') as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                "Назва",
                "Автор",
                "Ціна",
                "Посилання"
            )
        )

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/109.0.5414.120 Safari/537.36"
    }

    url = "https://www.yakaboo.ua/ua/knigi/komp-juternaja-literatura.html"

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    data = []

    pages_count = int(soup.find("div", class_="yb-pagination__nav-list").find_all("a")[-1].text)
    for i in range(1, pages_count + 1):
        url = f"https://www.yakaboo.ua/ua/knigi/komp-juternaja-literatura.html?p={i}"
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.content, 'lxml')

        items = soup.find_all('div', class_='category-card__content')
        for item in items:
            try:
                name = item.find('a', class_='category-card__name').text.strip()
            except Exception:
                name = 'no name'
            try:
                author = item.find('span', class_='creator-label').text.strip()
            except Exception:
                author = 'no author name'
            try:
                price = item.find('div', class_='ui-price-display__main').find('span').text.strip()
            except Exception:
                price = 'no price'

            try:
                url = 'https://www.yakaboo.ua' + item.find('a').get('href')
            except Exception:
                url = 'no url'

            data.append({
                'name': name,
                'author': author,
                'price': price,
                'url': url
            })
            with open(f"yakaboo_{cur_time}.csv", "a", encoding='UTF-8') as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        name,
                        author,
                        price,
                        url
                    )
                )
        time.sleep(1)
    with open(f'yakaboo_{cur_time}.json', 'w', encoding='UTF-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

get_data()
