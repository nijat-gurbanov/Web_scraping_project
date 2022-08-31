#####################################################################################
#####################     Web scraping using     ####################################
######################     Scrapy (part 1)     ######################################
#####################################################################################

# First spider to scrape the links
import scrapy

class Link(scrapy.Item):
    link = scrapy.Field()

class LinkListsSpider(scrapy.Spider):
    name = 'links'
    allowed_domains = ['https://basketball.realgm.com/']
    start_urls = ['https://basketball.realgm.com/nba/stats']

    def parse(self, response):
        xpath = '//tbody//@href'
        selection = response.xpath(xpath)
        for s in selection:
            l = Link()
            l['link'] = 'https://basketball.realgm.com' + s.get()
            yield l