import scrapy


class Article(scrapy.Item):


  title = scrapy.Field()
  author = scrapy.Field()
  text = scrapy.Field()
  date_pub = scrapy.Field(serializers=str)
  url = scrapy.Field()
  text_find = scrapy.Field()
  polarity = scrapy.Field(serializers=float)
  subjectivity = scrapy.Field(serializers=float)