import scrapy
from ..items import QuotetutsItem


class QuoteSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/',
    ]

    '''def parse_old(self, response):
        #title = response.css('title').extract()
        #title = response.css('title::text').extract_first()
        all_data = response.css('div.quote')[0]
        title = all_data.css('span.text::text').extract()
        author = all_data.css('small.author::text').extract()
        tags = all_data.css('a.tag::text').extract()
        yield {
            'title': title,
            'author': author,
            'tags': tags,
        }'''

    def parse(self, response):
        all_data = response.css('div.quote')
        items = QuotetutsItem()

        for quote in all_data:
            title = quote.css('span.text::text').extract()
            author = quote.css('small.author::text').extract()
            tags = quote.css('a.tag::text').extract()

            items['title'] = title
            items['author'] = author
            items['tag'] = tags

            yield items

            # now, we can trace all pages for the same
            next_page = response.css('li.next a::attr(href)').get()  # getting next page reference tag

            if next_page is not None:
                print('page_num: ', next_page)

                # following next page and recurse the parse() method to continuing scraping the data
                yield response.follow(next_page, callback=self.parse)
