##########################
# Currently not being used
##########################
import scrapy

class Article(scrapy.Item):
	title = scrapy.Field()
	authors = scrapy.Field()
	company = scrapy.Field()
	date_pub = scrapy.Field()
	body = scrapy.Field()
	positive = scrapy.Field(serializer=str)
	negative = scrapy.Field(serializer=str)
	url = scrapy.Field()

	def setPositive(self,percent):
		self.percent = percent
		self.negative = 1-double(percent)
		return

	def quantize():
		#Need to define a way to quantize each article
		return()