from pprint import pprint
import json
from pymongo import MongoClient
from lxml import html
import requests

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) YaBrowser/20.2.0.1145'}

# список масок XPath дла поиска новостей по сайтам
mask = {'yandex': {'site': "https://yandex.ru/news/",
                   'tag': "//div[@class='story__topic']",
                   'name': ".//h2[@class='story__title']/a/text()",
                   'source': "..//div[@class='story__info']/div[@class='story__date']/text()",
                   'date': "..//div[@class='story__info']/div[@class='story__date']/text()",
                   'href': ".//h2[@class='story__title']/a/@href"},

        'lenta': {'site': 'https://lenta.ru/',
                  'tag': "//div[@class='span4']//div[@class='item']//a",
                  #                     'tag': "//div[@class='span4']//div[@class='item']//a|//div[@class='span4']//div[@class='first-item']//a|//div[@class='row']//a//span",
                  'name': "./text()",
                  'source': ".//@href",
                  'date': ".//@datetime",
                  'href': ".//@href"},

        'mail': {'site': 'https://news.mail.ru/',
                 'tag': "//div[@class='block']//li//a",
                 'name': "./text()",
                 'source': "./text()",
                 'date': "./text()",
                 'href': ".//@href"}}


# вернуть список новостей с сайта site_name
def writenews_to_db(site_name):
    try:
        # скачать с сайта site_name все информационные теги по маске tag
        response = requests.get(mask[site_name]['site'], headers=header)
        root = html.fromstring(response.text)
        news_list = root.xpath(mask[site_name]['tag'])
        print('Всего на сайте новостей:', len(news_list))

        # по каждой найденной новости в списке разобрать значения
        for item in news_list:
            news_item = {}
            news_item['site'] = mask[site_name]['site']
            news_item['name'] = item.xpath(mask[site_name]['name'])[0]
            news_item['source'] = item.xpath(mask[site_name]['source'])[0]
            news_item['date'] = item.xpath(mask[site_name]['date'])[0]
            news_item['href'] = mask[site_name]['site'] + item.xpath(mask[site_name]['href'])[0]
            # специальная дообработка особенностей Яндекса
            if site_name == 'yandex':
                news_item['source'] = news_item['source'][:-5].replace('вчера', '').replace('\xA0в', '')
                news_item['date'] = news_item['date'][-5:]
            # специальная дообработка особенностей Мail
            if site_name == 'mail':
                news_item['source'] = "неизвестно"
                news_item['date'] = "неизвестно"
            # специальная дообработка особенностей Ленты
            if site_name == 'lenta':
                news_item['source'] = 'www.lenta.ru'
            # распечатать разобранную новость
            print(news_item['site'])
            print(news_item['name'])
            print(news_item['source'])
            print(news_item['date'])
            print(news_item['href'])

            # записать в базу данных новую уникальную новость
            if news.count_documents(news_item) == 0:
                news.insert_one(news_item)
            #                print('В базу данных добавлена новая строка с новостной информацией с сайта: ', news_item['site'])
            #                print(news_item)
            print()

        return
    except:
        print('Ошибка запроса')


# создаем базу данных "news" в MongoDB
client = MongoClient('localhost', 27017)
db = client['news']
news = db.news

# распарсить, распечатать и сохранить новости Яндекса
writenews_to_db('yandex')
writenews_to_db('mail')
writenews_to_db('lenta')




