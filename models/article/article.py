# This class will modelt articles

class Article:
	def __init__(self, company, date_pub, authors=None, sentp=0.0):
		self.company = company
		if authors is None:
			self.authors = []
		else:
			self.authors = authors
		self.date = date_pub
		self.positive = sentp
		self.negative = 1-sentp

	def quantize():
		#Need to define a way to quantize each article
		return()