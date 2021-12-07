import scrapy
from ..items import ScrapytutorialItem

class QuoteSpider(scrapy.Spider):
    name = "quotes"
    start_urls=[
        'https://quotes.toscrape.com/',
    ]

    def parse(self,response):


        items=ScrapytutorialItem()
        all_quotes = response.css("div.quote")
        for quote in all_quotes:
            title = quote.css("span.text::text").extract()
            author = quote.css("small.author::text").extract()
            tage = quote.css("a.tag::text").extract()

            items['title'] = title
            items['author'] = author
            items['tage'] = tage
            yield items
