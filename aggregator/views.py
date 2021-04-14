from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests

headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'referer': 'https://www.google.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44'
}
# Create your views here.


def get_the_news():
    url = 'https://in.news.yahoo.com/'
    articles = []

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    cards = soup.find_all('div', 'Py(14px)')

    for card in cards:
        title = "bello"
        title = card.find_all('a')[0].text
        link = card.find_all('a')[0].get('href')
        if link[0]!='h':
            link = "https://in.news.yahoo.com" + link
        # print(title.encode('utf-8'))
        c = card.find('img')
        image = ''
        if not c:
            c = card.find('div', 'Bdrs(2px)')
            img = c['style'].split(';')[1].split('(')[1]
            img = img[:-1]
            image = img
        else:
            if c.get('style'):
                img = c.get('style').split('(')[1]
                img = img[:-2]
                image = img
            else:
                image = c.get('src')
        if not image or len(title)<5:
            continue
        articles.append({"title":title, "image":image, "link":link})
    # for i in articles:
    #     print(i[0])
    return articles


def index(request):
    articles = get_the_news()
    return render(request, 'news/index.html', {'articles': articles})
