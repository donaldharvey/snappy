import datetime
class Image(object):
	def __init__(self, *args, **kwargs):
		self.id = 0
		self.name = ""
		self.category = 0 #FIXME
		self.tags = list() #FIXME
		self.path = ""
		self.timestamp = datetime.datetime.now()
