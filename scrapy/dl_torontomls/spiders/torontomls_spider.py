import scrapy
from dl_torontomls.items import Showing
import re

class TorontomlsSpider(scrapy.Spider):
    name = "torontomls"
    allowed_domains = ["openhouses.torontomls.net"]
    start_urls = [
        "http://openhouses.torontomls.net/poh/",
    ]

    def parse(self, response):
        for href in response.xpath("//map/area/@href"):
            url = href.extract()
            if url == 'regions/peel/index.htm':
                url = response.urljoin(url)
                yield scrapy.Request(url, callback=self.parseRegion)

    def parseRegion(self, response):
        for href in response.xpath("//map/area/@href"):
            url = href.extract()
            city = re.search(r"municip=([^=]*)", url).group(1)
            if url == '/poh/district_view?task=getPOHs&region=peel&municip=05.03':
                url = response.urljoin(url)
                yield scrapy.Request(url, meta={'city': city}, callback=self.parseCity)

    def parseCity(self, response):
        city = response.meta['city']
        for nodeDate in response.xpath('//tr[@bgcolor="#2B0069"]'):
            date = nodeDate.xpath('td/font/b/text()').extract()
            nodeCity = nodeDate.xpath('following-sibling::tr[1]')
            for nodeOh in nodeCity.xpath('following-sibling::tr[not (@bgcolor)]'):
                price = nodeOh.xpath('td[1]//text()').extract()[0]
                price = re.sub(r'[^\d]', '', price)

                url = nodeOh.xpath('td[2]//a/@href').extract()[0]
                url = re.search(r"'http://(.*)'", url).group(1)
                url = 'http://' + url

                listing_id = nodeOh.xpath('td[2]//a/text()').extract()[0]

                address = nodeOh.xpath('td[3]//text()').extract()[0].replace(u'\xa0', ' ').strip()
                unit_no = nodeOh.xpath('td[4]//text()').extract()[0].strip()
                start_tm = nodeOh.xpath('td[5]//text()').extract()[0]
                end_tm = nodeOh.xpath('td[6]//text()').extract()[0]

                agent_name = nodeOh.xpath('td[7]//text()').extract()[0]
                #ns = re.search(r"(.*),(.*)$", agent_name)
                #agent_name = ns.group(1).strip()
                #agent_position = ns.group(2).strip()

                agent_email = nodeOh.xpath('td[7]//a/@href').extract()[0]
                agent_email = re.search(r"mailto:(.*)\?", agent_email).group(1)

                broker_name = nodeOh.xpath('td[8]//text()').extract()[0]
                agent_phone = nodeOh.xpath('td[9]//text()').extract()[0]
                #if listing_id[0]=='W3379456':
                #    yield scrapy.Request(url, callback=self.parseDetail)

                showing = Showing(
                    listing_id = listing_id,
                    price = price,
                    listing_url = url,
                    start_tm = start_tm,
                    end_tm = end_tm,
                    address = address,
                    unit_no = unit_no,
                    city = city,
                    agent_name = agent_name,
                    agent_email = agent_email,
                    agent_phone = agent_phone,
                    broker_name = broker_name)
                yield showing

    def parseDetail(self, response):
        pass
