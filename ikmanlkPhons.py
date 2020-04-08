# -*- coding: utf-8 -*-
import scrapy


class MobilephonesSpider(scrapy.Spider):
    name = 'mobilephones'
    allowed_domains = ['ikman.lk/en/ads/sri-lanka/mobile-phones']
    start_urls = ['http://ikman.lk/en/ads/sri-lanka/mobile-phones']
    absolute_url = 'http://ikman.lk'
    page_number = 2

    def parse(self, response):
        all_phones = response.xpath('//li[@class ="normal--2QYVk gtm-normal-ad"]')
        for phone in all_phones:
            phone_url = self.absolute_url+phone.xpath('.//a/@href').extract_first()
            yield scrapy.Request(phone_url, callback=self.inside_phone, dont_filter=True)

        next_page = self.start_urls[0] + '?by_paying_member=0&sort=date&order=desc&buy_now=0&page=' + str(self.page_number)
        if self.page_number<10:
            yield scrapy.Request(next_page, callback=self.parse, dont_filter=True)
            self.page_number += 1

    def inside_phone(self, response):
        name = response.xpath('//div[@class="item-top col-12 lg-8"]/h1/text()').extract_first()
        price =response.xpath('//span[@class="amount"]/text()').extract_first()
        description = response.xpath('//div[@class="item-description"]/p/text()').extract_first()
        contact_number = response.xpath('//span[@class="h3"]/text()').extract_first()
        location = response.xpath('//span[@class="location"]/text()').extract_first()
        saler_name = response.xpath('//span[@class="poster"]/text()').extract_first()
        date = response.xpath('//span[@class="date"]/text()').extract_first()
        condition = response.xpath('//div[@class="item-properties"]/dl[1]/dd/text()').extract_first()
        brand = response.xpath('//div[@class="item-properties"]/dl[2]/dd/text()').extract_first()
        model = response.xpath('//div[@class="item-properties"]/dl[3]/dd/text()').extract_first()
        edition = response.xpath('//div[@class="item-properties"]/dl[4]/dd/text()').extract_first()
        features = response.xpath('//div[@class="item-properties"]/dl[5]/dd/text()').extract_first()

        yield {
            'Phone Name': name,
            'Price': 'Rs ' + str(price),
            'Description': description,
            'Contact Number': contact_number,
            'Location': location,
            'Saler Name': saler_name,
            'Sell Date':date,
            'Condition': condition,
            'Brand': brand,
            'Model': model,
            'Edition': edition,
            'Features': features
        }





