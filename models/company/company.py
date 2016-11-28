##########################
# Currently not being used
##########################
class Company:

	def __init__(self, name, authors):
		self.name = name
		if authors is None:
			self.authors=[]
		else:
			self.authors=authors
		self.auth_grades = []

	def add_author(self,author):
		self.authors.append(author)