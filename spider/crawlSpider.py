from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class someSpider(CrawlSpider):
  name = 'crawltest'
  allowed_domains = [r'cnn.com']
  start_urls = ['http://money.cnn.com/']

  rules = (Rule(LinkExtractor(allow=()), callback='parse_obj', follow=True),)


  def parse_obj(self,response):
    for link in LinkExtractor(allow=self.allowed_domains,deny = ()).extract_links(response):
    	if "index" in link.url:
    		yield{
				'text':link.text,
				'url':link.url
			}
#        item = someItem()
#        item['url'] = link.url