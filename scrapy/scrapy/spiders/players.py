#####################################################################################
#####################     Web scraping using     ####################################
######################     Scrapy (part 2)     ######################################
#####################################################################################

# Second spider to scrape the information from each players' profile
import scrapy
import re

class Player(scrapy.Item):
    name        = scrapy.Field()
    curr_team   = scrapy.Field()
    age         = scrapy.Field()
    national    = scrapy.Field()
    height      = scrapy.Field()
    weight      = scrapy.Field()

class LinksSpider(scrapy.Spider):
    name = 'players'
    allowed_domains = ['https://basketball.realgm.com/']
    try:
        with open("links.csv", "rt") as f:
            start_urls = [url.strip() for url in f.readlines()][1:]
    except:
        start_urls = []

    def parse(self, response):
        players = Player()

        players['name']         = response.xpath('//*[@class="profile-box"]//h2/text()').get().replace('\xa0','')
        players['curr_team']    = response.xpath('//*[text()="Current Team:"]/following-sibling::*/text()').get()
        players['age']          = response.xpath('//*[text()="Born:"]/parent::*/text()').getall()[1][2:4]
        players['national']     = response.xpath('//*[text()="Nationality:"]/following-sibling::*/text()').get()
        players['height']       = re.findall(r'\((.*?)\)', response.xpath('//*[text()="Height:"]/parent::*/text()').getall()[0])[0].replace('cm','')
        players['weight']       = re.findall(r'\((.*?)\)', response.xpath('//*[text()="Height:"]/parent::*/text()').getall()[1])[0].replace('kg','')

        yield players