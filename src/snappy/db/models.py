from sqlobject import *

class Model:
	class Image(SQLObject):
		name = StringCol(length = 255)
		category = ForeignKey('Category')
		tags = RelatedJoin('Tag')
		path = StringCol(notNone = True)
		timestamp = DateTimeCol(notNone=True)
		type = StringCol(length = 255, notNone = True) # MIME type of the image.
		url = StringCol() # Image's URL, if it exists. 
		rating = IntCol() # Rating out of five
		def _get_imagedata(self):
			f = open(self.path, 'rb')
			data = image.read()
			f.close()
			return data
		def _set_imagedata(self, value):
			imagedata = value # clearer variable name
			f = open(self.path, 'w')
			f.write(imagedata)
			f.close()
			return True
		
	class Category(SQLObject):
		name = StringCol(length = 255)
		parent = IntCol(notNone = False)
		
	class Tag(SQLObject):
		name = StringCol(length = 255)
