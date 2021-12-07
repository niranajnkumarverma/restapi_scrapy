import scrapy
from ..items import AmazonscrapingItem


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.in/s?i=stripbooks&bbn=976389031&rh=n%3A976389031%2Cp_n_feature_three_browse-bin%3A9141482031%7C9141484031%2Cp_36%3A1741392031&dc&qid=1631818079&rnid=9141481031&ref=sr_nr_p_n_feature_three_browse-bin_1']

    def parse(self, response):
        item = AmazonscrapingItem()
        title = response.css('.a-text-normal::text').extract()
        author = response.css('.a-size-base::text').extract()
        price = response.css('.a-price-whole::text').extract()
        image_link = response.css('.s-image::attr(src)').extract()



        item['title'] = title
        item['author'] = author
        item['price'] = price
        item['image_link'] = image_link

        yield item
