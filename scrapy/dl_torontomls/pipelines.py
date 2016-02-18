# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
from scrapy import signals
from scrapy.exporters import XmlItemExporter
from scrapy.exporters import CsvItemExporter

class CsvExportPipeline(object):
    def __init__(self):
        self.brokers = []

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.brokers_csv = open('brokers.csv', 'w')
        self.exporter = CsvItemExporter(self.brokers_csv)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        brokers = set(self.brokers)
        for broker in brokers:
            self.exporter.export_item(broker)
        self.exporter.finish_exporting()
        self.brokers_csv.close()

    def process_item(self, item, spider):
        self.brokers.append(item['broker_name'])
        return item


class XmlExportPipeline(object):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('%s_showings.xml' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = XmlItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

class DlTorontomlsPipeline(object):
    def __init__(self):
        self.url = 'http://localhost:8069'
        self.db = 'test'
        self.username = 'admin'
        self.password = 'shawnN'

        self.common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
        print self.common.version()
        self.uid = self.common.authenticate(self.db, self.username, self.password, {})
        print self.uid

        self.models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.url))

    def execute(self, model, command, parameter):
        return self.models.execute_kw(self.db, self.uid, self.password, model, command, parameter)

    def process_item(self, listing, spider):
        agent = listing['agent']
        email = re.search(r"mailto:(.*)\?", agent['email']).group(1)
        name = agent['name']
        ns = re.search(r"(.*),(.*)$", name)
        name = ns.group(1).strip()
        position = ns.group(2).strip()
        print "{}\t{}".format(name, position)
        ids = self.execute('res.partner', 'search', [[['email', '=', email]]])

        if len(ids) == 0:
            id = self.execute('res.partner', 'create', [{
                'name': name,
                'email': email
            }])
        elif len(ids) == 1:
            id = ids[0]
            #self.execute('res.partner', 'unlink', [[id]])
        else:
            print "duplicated email: {} found".format(agent['email'])

        self.execute('res.partner', 'write', [[id], {
            'phone': agent['phone'],
            'function': position
        }])

        return listing
