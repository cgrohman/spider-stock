from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
from html.parser import HTMLParser
import re

XPATH_SELECTOR = '//*[@id="storytext"]/*[self::h2 or self::p]'
AUTHOR_CSS = '.byline::text'
AUTHOR_CSS_A = '.byline a::text'
DATE_CSS = '.cnnDateStamp::text'
DENY = [r'/quote.*',r'/video.*',r'/services/privacy/',r'/services/terms.html']
ALLOW = [r'money.cnn.com']
TEXT_FIND = r'trump'


class NewsSpider(CrawlSpider):
	name = 'crawltest'
	allowed_domains = [r'money.cnn.com']
	deny_domains = [r'com/quote']
	start_urls = ['http://money.cnn.com/']
	rules = (Rule(LinkExtractor(allow=ALLOW, deny = DENY), callback='parse_page', follow=True),)

	def parse_page(self,response):
		regex = re.compile(TEXT_FIND, re.IGNORECASE)
		text = response.xpath(XPATH_SELECTOR).extract()
		text = ''.join(text)
		if regex.search(text) is None: return
		text = strip_tags(text)
		author = response.css(AUTHOR_CSS_A).extract_first()
		if author is None:
			author = response.css(AUTHOR_CSS).extract_first()
			author = re.sub('by ','',author)
		date_pub = response.css(DATE_CSS).extract_first()
		yield{'text':text,
			'author':author.strip(),
			'link':response.url,
			'date':date_pub.strip()}

#Used for stripping text of html tags, returns only text
class MLStripper(HTMLParser):
	def __init__(self):
		super().__init__()
		self.reset()
		self.fed = []
	def handle_data(self, d):
		self.fed.append(d)
	def get_data(self):
		return ''.join(self.fed)

# Strips string of html tags
def strip_tags(html):
	s = MLStripper()
	s.feed(html)
	return s.get_data()