# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo[c][0]=1']

    def parse(self, response: HtmlResponse):
 #       next_page = response.css('a.f-test-button_active::attr(href)').extract_first()
        next_page = response.xpath("// a[@class='icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe']//@href").extract_first()
 #       next_page = response.xpath("//div[@class='L1p51']//a//@href").extract_first()
        print('Следующая страница: ', next_page)
        yield response.follow(next_page, callback=self.parse)
        vacansy = response.xpath("//div[@class='_3syPg _3P0J7 _9_FPy']//@href").extract()
#        vacansy = response.css(
#            'div._3MVeX::attr(href)'
#        ).extract()
        print('Список вакансий: ', vacansy)
        for link in vacansy:
            yield response.follow(link, callback=self.vacansy_parse)

    def vacansy_parse(self, response: HtmlResponse):
#        name = response.css('div.vacancy-title h1.header::text').extract_first()
#        salary = response.css('div.vacancy-title p.vacancy-salary::text').extract()
#        print('Ссылка: ', response.url)
        name = response.xpath("//div[@class='_3MVeX']//h1//text()").extract_first()
        salary = response.xpath("//div[@class='_3MVeX']//span[@class='_3mfro _2Wp8I ZON4b PlM3e _2JVkc']//text()").extract()
        link = response.url
#        print('Вакансия: ', name, salary, link)
        if name != None:
            yield JobparserItem(name=name, salary=salary, link=link, source='superjob.ru')
