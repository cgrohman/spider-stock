#######################################################################
# Author: Cori Grohman
# Date: 11/27/2016
#######################################################################
# Description: 
#	- To test this spider, you can run the following command:
#		$: scrapy runspider newsSpider.py -o output.json
#	- To alter the search topic, change the variable "TEXT_FIND"
#	- Output will be located in the "output.json" file
# To-Do:
#	- Implement input parameters for domain specific searches
#	- Import database functions from /utils for storage
#	- Breakout text/author/date/url logic into functions for input 
#		parameter based logic		
# This iteration is simply for testing purposes, it allows for testing
# of the crawling functionality along with xpath/csspath testing
#######################################################################

from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
from html.parser import HTMLParser
import re

DATE_CSS = '.cnnDateStamp::text'
DENY = [r'/quote.*',r'/video.*',r'/services/privacy/',r'/services/terms.html']
ALLOW = [r'money.cnn.com']
TEXT_FIND = r'trump'

class NewsSpider(CrawlSpider):
	name = 'crawltest'
	start_urls = ['http://money.cnn.com/']

	XPATH_SELECTOR = '//*[@id="storytext"]/*[self::h2 or self::p]'
	AUTHOR_CSS = '.byline::text'
	AUTHOR_CSS_A = '.byline a::text'
	regex = re.compile(TEXT_FIND, re.IGNORECASE)

	rules = (Rule(LinkExtractor(allow=ALLOW, deny = DENY), callback='parse_page', follow=True),)

	def parse_page(self,response):
		article_text = self.get_text(response)
		if article_text is None: 
			#log cannot find error
			return
		author_text = self.get_author_text(response)
		if author_text is None:
			author_text = 'NA'
		date_pub = response.css(DATE_CSS).extract_first()
		yield{'text':article_text,
			'author':author_text.strip(),
			'link':response.url,
			'date':date_pub.strip()}

	def get_text(self,response):
		text_list = response.xpath(self.XPATH_SELECTOR).extract()
		if not text_list: return None
		text = ''.join(text_list)
		article_text = strip_tags(text)
		return article_text

	def get_author_text(self,response):
		author_text = response.css(self.AUTHOR_CSS_A).extract_first()
		if author_text is None:
			author = response.css(self.AUTHOR_CSS).extract_first()
			if author is None: return None
			author_text = re.sub('by ','',author)
		return author_text

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