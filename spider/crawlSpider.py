from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
from pymongo import MongoClient

CSS_SELECTOR = 'p , h2'
TEXT_FIND = r'tesla'

class someSpider(CrawlSpider):
  name = 'crawltest'
  allowed_domains = [r'cnn.com']
  start_urls = ['http://money.cnn.com/']

  rules = (Rule(LinkExtractor(allow=()), callback='parse_link', follow=True),)

  def parse_link(self,response):
    for link in LinkExtractor(allow=self.allowed_domains,deny = ()).extract_links(response):
    	if "index" in link.url:
    		return scrapy.Request(link.url,callback=self.parse_page)

  def parse_page(self,response):
    regex = re.compile(TEXT_FIND, re.IGNORECASE)
    for text in response.css(CSS_SELECTOR):
      if regex.search(text) is not None:
        #save text for text processing later