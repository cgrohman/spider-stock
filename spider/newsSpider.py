#######################################################################
# Author: Cori Grohman
# Date: 11/27/2016
#######################################################################
# Description: 
# - To test this spider, you can run the following command:
#   $: scrapy runspider newsSpider.py -o output.json
# - Output will be located in the "output.json" file
# To-Do:
# - Implement input parameters for domain specific searches
# - Import database functions from /utils for storage
# - Breakout text/author/date/url logic into functions for input 
#   parameter based logic   
# This iteration is simply for testing purposes, it allows for testing
# of the crawling functionality along with xpath/csspath testing
#######################################################################

from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
import re
from items import Article
import env_config
import pipelines


class NewsSpider(CrawlSpider):


  name = 'crawlTest'
  custom_settings={
    'MONGODB_SERVER' : "localhost",
    'MONGODB_PORT' : 27017,
    'MONGODB_DB' : "SPIDER_STOCK",
    'MONGODB_COLLECTION' : "articles",
    'ITEM_PIPELINES' : {
      'pipelines.MongoDBPipeline':100,
      }
  }
  domain_key = env_config.DOMAIN_NAME
  start_urls = env_config.DOMAIN_DICT[domain_key]['start_url']
  allow = env_config.DOMAIN_DICT[domain_key]['allow']
  deny = env_config.DOMAIN_DICT[domain_key]['deny']
  if not env_config.DOMAIN_DICT[domain_key]['article_xpath_sel']:
    article_xpath_sel = None
  else:
    article_xpath_sel = env_config.DOMAIN_DICT[domain_key]['article_xpath_sel']
  if not env_config.DOMAIN_DICT[domain_key]['article_css_sel']:
    article_css_sel = None
  else:
    article_css_sel = env_config.DOMAIN_DICT[domain_key]['article_css_sel']
  if not env_config.DOMAIN_DICT[domain_key]['author_css_sel']:
    author_css_sel = None
  else:
    author_css_sel = env_config.DOMAIN_DICT[domain_key]['author_css_sel']
  if not env_config.DOMAIN_DICT[domain_key]['author_xpath_sel']:
    author_xpath_sel = None
  else:
    author_xpath_sel = env_config.DOMAIN_DICT[domain_key]['author_xpath_sel']
  if not env_config.DOMAIN_DICT[domain_key]['date_xpath_sel']:
    date_xpath_sel = None
  else:
    date_xpath_sel = env_config.DOMAIN_DICT[domain_key]['date_xpath_sel']
  if not env_config.DOMAIN_DICT[domain_key]['date_css_sel']:
    date_css_sel = None
  else:
    date_css_sel = env_config.DOMAIN_DICT[domain_key]['date_css_sel']
  if not env_config.DOMAIN_DICT[domain_key]['title_css']:
    title_css = None
  else:
    title_css = env_config.DOMAIN_DICT[domain_key]['title_css']
  text_find = env_config.REG_FIND
  regex = re.compile(text_find, re.IGNORECASE)
  rules = (Rule(LinkExtractor(allow=allow, deny =deny), callback='_parse_page', follow=True),)

  def _parse_page(self,response):

    article_text = self._get_article_text(response)
    if article_text is None: 
      #log cannot find error
      return
    if not self._interest_in_article(article_text): return
    author_text = self._get_author_text(response)
    if author_text is None:
      author_text = 'NA'
    date_pub = self._get_date_pub(response)
    if date_pub is None:
      date_pub = 'NA'
    title_text = self._get_title_text(response)
    if title_text is None:
      title_text = 'NA'
    current_article = Article(text=article_text, author= author_text.strip(),url=response.url, date_pub=date_pub.strip(), title=title_text.strip(),text_find=self.text_find)
    yield current_article

  def _get_article_text(self,response):

    if self.article_xpath_sel is not None:
      text_list = response.xpath(self.article_xpath_sel).extract()
    elif self.article_css_sel is not None:
      text_list = response.css(self.article_css_sel).extract()
    if text_list is None: return None
    text = ''.join(text_list)
    return text

  def _get_author_text(self,response):

    for css_sel in self.author_css_sel:
      author_text = response.css(css_sel).extract_first()
      if author_text is None: continue
      author_text = re.sub('by ','',author_text)  
      return author_text

  def _get_date_pub(self,response):

    return response.css(self.date_css_sel).extract_first()

  def _get_title_text(self,response):

    return response.css(self.title_css).extract_first()

  def _interest_in_article(self,article):

    if self.regex.search(article) is not None:
      return True
    return False
