# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://izhevsk.hh.ru/search/vacancy?area=&st=searchVacancy&text=python']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
#        next_page = response.xpath("//a[@class='HH-Pager-Controls-Next']@href").extract_first()
        print('Слдующая страница:  ', next_page)
        yield response.follow(next_page, callback=self.parse)

        vacansy = response.css(
            'div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header a.bloko-link::attr(href)'
        ).extract()
#        vacansy = response.xpath("//div[@class='vacancy-serp vacancy-serp-item vacancy-serp-item__row_header']//a[@class='bloko-link']@href").extract()
        print('Перечень вакансий: ', vacansy)
        for link in vacansy:
            yield response.follow(link, callback=self.vacansy_parse)

    def vacansy_parse(self, response: HtmlResponse):
#        name = response.css('div.vacancy-title h1.header::text').extract_first()
#        salary = response.css('div.vacancy-title p.vacancy-salary::text').extract()
#        print('link: ', response.url)
        name = response.xpath("//div[@class='vacancy-title']//h1/text()").extract_first()
        salary = response.xpath("//div[@class='vacancy-title']//p[@class='vacancy-salary']//text()").extract()
        link = response.url
#        print('Вакансия: ', name, salary, link)
        if name != None:
            yield JobparserItem(name=name, salary=salary, link=link, source='hh.ru')


