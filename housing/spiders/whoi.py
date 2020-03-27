# -*- coding: utf-8 -*-
import scrapy


def stripExtraSpace(toStrip):
    return ' '.join(toStrip.split())

class WhoiSpider(scrapy.Spider):
    name = 'whoi'
    allowed_domains = ['www.whoi.edu']

    def start_requests(self):
        yield scrapy.Request('https://www.whoi.edu/housing/housingListing.do', self.parse)

    def parse(self, response):
        item = {}
        listings = response.xpath('//div[@id="cof"]/table/tr/td/form/table//tr')
        # print(listings)
        # Ignore table header row
        for listing in listings[1:]:
            item = dict()
            item['Date Posted'] = listing.xpath('td[2]//text()').get()
            item['Description'] = listing.xpath('td[3]//text()').get()
            item['Location'] = listing.xpath('td[4]//text()').get()
            item['Rent'] = listing.xpath('td[5]//text()').get()
            item['Season'] = listing.xpath('td[6]//text()').get()
            item['Availability'] = listing.xpath('td[7]//text()').get()
            moreinfo = listing.xpath('td[8]//@href').get()

            request = scrapy.Request(response.urljoin(moreinfo), callback=self.parse_more_info)
            request.meta['item'] = item

            yield request

    def parse_more_info(self, response):
        item = response.meta['item']

        response = response.replace(body=response.body.replace(b'<br>', b'\n'))
        response = response.replace(body=response.body.replace(b'\r\n', b''))

        item['Details'] = stripExtraSpace(response.xpath('string(//div[@id="cof"]/table/tr/td/table/tr[2]//td[2])').get())
        item['Contact'] = stripExtraSpace(response.xpath('string(//div[@id="cof"]/table/tr/td/table/tr[2]//td[3])').get())

        yield item
