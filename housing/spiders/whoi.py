# -*- coding: utf-8 -*-
import datetime

import scrapy

from housing.items import HousingItem


def strip_extra_space(to_strip: str) -> str:
    return ' '.join(to_strip.split())


class WhoiSpider(scrapy.Spider):
    name = 'whoi'
    allowed_domains = ['www.whoi.edu']

    def start_requests(self):
        yield scrapy.Request('https://www.whoi.edu/housing/housingListing.do', self.parse)

    def parse(self, response):
        item = HousingItem()
        listings = response.xpath('//div[@id="cof"]/table/tr/td/form/table//tr')

        # Ignore table header row
        for listing in listings[1:]:
            date_posted_string = listing.xpath('td[2]//text()').get()
            item['date_posted'] = datetime.datetime.strptime(date_posted_string, "%Y-%m-%d").date()
            item['description'] = listing.xpath('td[3]//text()').get()
            item['location'] = listing.xpath('td[4]//text()').get()
            item['rent'] = listing.xpath('td[5]//text()').get()
            item['season'] = listing.xpath('td[6]//text()').get()
            item['availability'] = listing.xpath('td[7]//text()').get()
            moreinfo = listing.xpath('td[8]//@href').get()

            request = scrapy.Request(response.urljoin(
                moreinfo), callback=self.parse_more_info)
            request.meta['item'] = item

            yield request

    def parse_more_info(self, response):
        item = response.meta['item']

        response = response.replace(body=response.body.replace(b'<br>', b'\n'))
        response = response.replace(body=response.body.replace(b'\r\n', b''))

        item['details'] = strip_extra_space(response.xpath(
            'string(//div[@id="cof"]/table/tr/td/table/tr[2]//td[2])').get())
        item['contact'] = strip_extra_space(response.xpath(
            'string(//div[@id="cof"]/table/tr/td/table/tr[2]//td[3])').get())

        yield item
