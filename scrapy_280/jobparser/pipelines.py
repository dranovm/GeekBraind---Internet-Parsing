# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import re

class JobparserPipeline(object):

    def __init__(self):
        client = MongoClient('localhost',27017)
        self.mongobase = client.vacansy_280

#    def hhru_convert(item):
#
#        if item["salary"][0] == 'з/п не указана':
#            pass
#        elif item["salary"][0] == 'до':
#            salary_max = item['salary'][1]
#            salary_currency = item['salary'][3]
#        elif item["salary"][0] == 'от':
#            salary_min = item['salary'][1]
#            if ['salary'][2] == 'до':
#               salary_max = item['salary'][3]
#               salary_currency = item['salary'][5]
#            else:
#               salary_currency = item['salary'][3]
#        else:
#            pass
#
#        item_rec = {'name': item['name'],
#                    'source': item['source'],
#                    'link': item['link'],
#                    'salary_min': salary_min,
#                    'salary_max': salary_max,
#                    'salary_currency': salary_currency}
#        print(item_rec)
#        return item_rec


#    def sjru_convert(item):
#        print("Получил в процесс : ", item)
#        if item["salary"][0] == 'По договорённости':
#            pass
#        elif item["salary"][0] == 'до':
#            salary_max = item['salary'][2]
#            salary_currency = item['salary'][4]
#        elif item["salary"][0] == 'от':
#            salary_min = item['salary'][2]
#            salary_currency = item['salary'][4]
#        elif item["salary"][2] == '—':
#           salary_min = item['salary'][0]
#            salary_max = item['salary'][4]
#            salary_currency = item['salary'][6]
#        else:
#            pass
#            self.sjru_convert(item)
#        item_rec = {'name': item['name'],
#                      'source': item['source'],
#                      'link': item['link'],
#                      'salary_min': salary_min,
#                      'salary_max': salary_max,
#                      'salary_currency': salary_currency}
#        print(item_rec)
#        return item_rec

    def process_item(self, item, spider):
        """

        :type item: object
        """
        for i in range(len(item["salary"])):
            item['salary'][i]  = item["salary"][i].replace('\xa0',' ')
        salary_min = None
        salary_max = None
        salary_currency = None
#        if spider.name == 'hhru':
#            salary_rec = hhru_convert(item)
#        print('Исходные данные:', item)
        if item['source'] == 'hh.ru':
            if item["salary"][0]=='з/п не указана':
                pass
            elif item["salary"][0]=='до':
                salary_max=item['salary'][1]
                salary_currency=item['salary'][3]
            elif item["salary"][0]=='от':
                salary_min=item['salary'][1]
                if ['salary'][2]=='до':
                    salary_max = item['salary'][3]
                    salary_currency = item['salary'][5]
                else:
                    salary_currency=item['salary'][3]
#        if spider.name == 'sjru':
#            salary_rec = sjru_convert(item)
        elif item['source'] == 'superjob.ru':
            if item["salary"][0]=='По договорённости':
                pass
            elif item["salary"][0]=='до':
                salary_max=item['salary'][2]
                salary_currency=item['salary'][4]
            elif item["salary"][0]=='от':
                salary_min=item['salary'][2]
                salary_currency=item['salary'][4]
            elif item["salary"][2]=='—':
                salary_min=item['salary'][0]
                salary_max=item['salary'][4]
                salary_currency=item['salary'][6]
        salary_rec = { 'name': item['name'],
                       'source': item['source'],
                       'link': item['link'],
                       'salary_min': salary_min,
                       'salary_max': salary_max,
                       'salary_currency': salary_currency}
        print("Сохраняю вакансию : ", salary_rec)
        collection = self.mongobase[spider.name]
        collection.insert_one(salary_rec)

        return item
