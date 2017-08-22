# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class TianqiPipeline(object):

    def open_spider(self, spider):
        self.file = open('weather.json', 'w')

    def process_item(self, item, spider):

        data = json.dumps(dict(item), ensure_ascii=False, indent=2)

        self.file.write(data)

        return item

    def close_spider(self, spider):
        self.file.close()