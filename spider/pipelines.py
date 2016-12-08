import pymongo
import settings
from textblob import TextBlob
from scrapy.exceptions import DropItem
from scrapy import log
from html.parser import HTMLParser

class MongoDBPipeline(object):

  def __init__(self):
    connection = pymongo.MongoClient(
      settings.MONGODB_SERVER,
      settings.MONGODB_PORT
    )
    db = connection[settings.MONGODB_DB]
    self.collection = db[settings.MONGODB_COLLECTION]

  def process_item(self, item, spider):

    valid = True
    for data in item:
      if not data:
        valid = False
        raise DropItem("Missing {0}!".format(data))
    if valid:
      #clean article data
      item = self._clean_text(item, spider)
      item = self._get_sentiment(item, spider)
      self.collection.insert(dict(item))
      log.msg("Article added to MongoDB database",
          level=log.DEBUG, spider=spider)
    return item

  def _clean_text(self, item, spider):

    try:
      item['text'] = stripTags(item['text'])
      item['text'] = re.sub(r'\\','',item['text'])
    except:
      log.msg("Unable to clean text: {}".format(item['title'],level=log.ERROR,spider=spider))
    return item

  def _get_sentiment(self,item,spider):

    try:
      text_blob = TextBlob(item['text'])
    except:
      log.msg("'_get_sentiment' failed to get text: {}".format(item['title'],level=log.ERROR,spider=spider))
    item['polarity'] = text_blob.sentiment.polarity
    item['subjectivity'] = text_blob.sentiment.subjectivity
    return item

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
def stripTags(html):

  s = MLStripper()
  s.feed(html)
  return s.get_data()
