from sqlobject import *

class Model:
	class Capture(SQLObject):
		name = StringCol(length = 255)
		category = ForeignKey('Category')
		tags = RelatedJoin('Tag')
		path = StringCol(notNone = True)
		timestamp = DateTimeCol(notNone=True)
		mimetype = StringCol(length = 255, notNone = True) # MIME type of the capture.
		type = StringCol(length = 2) # Two-letter representation of the type of capture (screencast, area, window etc)
		url = StringCol() # Image's URL, if it exists. 
		rating = IntCol() # Rating out of five
		def _get_data(self):
			f = open(self.path, 'rb')
			data = image.read()
			f.close()
			return data
		def _set_data(self, value):
			data = value # clearer variable name
			f = open(self.path, 'w')
			f.write(data)
			f.close()
			return True
		
	class Category(SQLObject):
		name = StringCol(length = 255)
		parent = IntCol(notNone = False)
		icon = StringCol()
		
	class Tag(SQLObject):
		name = StringCol(length = 255)
