# -*- coding: utf-8 -*-
import scrapy
import time

from TianQi.items import TianqiItem


class WeatherSpider(scrapy.Spider):
    name = 'weather'
    allowed_domains = ['tianqi.com']
    start_urls = ['http://lishi.tianqi.com/']

    def parse(self, response):

        # 获取所有地区的列表
        area_list = response.xpath("//div[@id='tool_site']/div[2]/ul/li/a/text()").extract()

        # 获取所有地区的链接
        url_list = response.xpath("//div[@id='tool_site']/div[2]/ul/li/a/@href").extract()

        # 遍历地区列表和url列表
        for area, url in zip(area_list, url_list):
            # 对url进行判断 看是否为 #
            # print area,"------",url
            if url == '#':
                continue
            # 创建请求并发送
            yield scrapy.Request(url, callback=self.parse_area, meta={'area_name': area})

    def parse_area(self, response):
        # 接收meta传来的地区名
        area = response.meta['area_name']
        # print area

        # 获取每一个月份url列表
        url_list = response.xpath("//*[@id='tool_site']/div[2]/ul/li/a/@href").extract()
        # 遍历url列表
        for url in url_list:
            # 创建请求并发送
            # print url
            yield scrapy.Request(url, callback=self.parse_data, meta={'area_name': area})

    def parse_data(self, response):
        # 接收meta传来的地区名
        area = response.meta['area_name']
        # print area, '---', response.url
        data_list = response.xpath("//*[@id='tool_site']/div[@class='tqtongji2']/ul")
        print len(data_list),'---'

        # 循环遍历取出数据
        for data in data_list:

            # 实例化item对象
            item = TianqiItem()
            item['area'] = area
            item['url'] = response.url
            item['timestamp'] = time.time()
            item['date'] = data.xpath("./li[1]/text()").extract_first()
            if item['date'] == None:
                item['date'] = data.xpath("./li[1]/a/text()").extract_first()

            item['max_t'] = data.xpath("./li[2]/text()").extract_first()
            item['min_t'] = data.xpath("./li[3]/text()").extract_first()
            item['weather'] = data.xpath("./li[4]/text()").extract_first()
            item['wind_direction'] = data.xpath("./li[5]/text()").extract_first()
            item['wind_power'] = data.xpath("./li[6]/text()").extract_first()

            yield item