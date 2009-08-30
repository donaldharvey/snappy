import datetime
class Model(object):
	class Image(object):
		def __init__(self):
			self.id = int
			self.name = str
			self.category = int
			self.tags = list #FIXME
			self.path = str
			self.timestamp = datetime.datetime
			
			# Database stuff.
			self._pk = 'id'
	class Category(object):
		def __init__(self):
			self.id = int
			self.name = str
			self._plural = ('categories')
	sql = '''
	create table images(
		text name,
		text category,
		text tags,
		text path,
		date timestamp,
	)
	create table categories(
		text name
	)