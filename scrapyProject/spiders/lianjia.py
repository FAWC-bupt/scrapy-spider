import scrapy

from scrapyProject.items import ScrapyprojectItem


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['bj.lianjia.com']
    base_url = 'https://bj.lianjia.com/ershoufang/'
    zones = ['dongcheng/', 'xicheng/', 'chaoyang/', 'haidian/']
    zones_chinese = ['东城', '西城', '朝阳', '海淀']
    page_index = 1  # 页面计数
    zone_index = 1  # 地区计数
    start_urls = [base_url + zones[0]]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.download_delay = 5

    def parse(self, response, **kwargs):
        item = ScrapyprojectItem()

        info_list = response.xpath('//div[@class="info clear"]')
        for info in info_list:
            item['zone_name'] = self.zones_chinese[self.zone_index - 1]
            item['building_names'] = info.xpath('./div[@class="flood"]/div[@class="positionInfo"]/a[1]/text()').get()
            # print(item['building_names'])
            item['total_price'] = ''.join(info.xpath(
                './div[@class="priceInfo"]/div[@class="totalPrice"]/span/text()').getall() + info.xpath(
                './div[@class="priceInfo"]/div[@class="totalPrice"]/text()').getall())
            # print(item['total_price'])
            item['area'] = info.xpath(
                './div[@class="address"]/div[@class="houseInfo"]/text()').get().split('|')[1].strip()
            # print(item['area'])
            item['price_per_area'] = info.xpath(
                './div[@class="priceInfo"]/div[@class="unitPrice"]/span/text()').get()
            # print(item['price_per_area'])

            if item['building_names'] and item['total_price'] and item['area'] and item['price_per_area']:
                yield item

        self.page_index += 1
        if self.zone_index < len(self.zones):
            if self.page_index <= 5:
                url = self.base_url + self.zones[self.zone_index] + 'pg' + str(self.page_index)
            else:
                self.page_index = 1
                url = self.base_url + self.zones[self.zone_index]
                self.zone_index += 1
        else:
            return
        yield scrapy.Request(url, callback=self.parse)
