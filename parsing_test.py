from bs4 import BeautifulSoup
import requests

n = 0
for page in range(1,11):
    url = f'https://24.kg/page_{page}'
    response = requests.get(url=url)
    # print(response.text)
    soup = BeautifulSoup(response.text,'lxml')
    all_news = soup.find_all('div',class_='title')
    # print(all_news)
    for news in all_news:
        n += 1
        print(n,news.text)

