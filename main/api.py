#!/usr/bin/env python
class API:
	class Image:
		filename = "" 
		mimetype = ""
		path = "" #abs. path to file
		size = (0, 0) #2-tuple of width, height
		filesize = 0 #in bytes
		title = ""
	class Video:
		filename = ""
		mimetype = ""
		path = "" #abs. path to file
		size = (0, 0) #2-tuple of width, height
		filesize = 0 #in bytes
		duration = 0 #in seconds
		title = ""
	image = Image()
	video = Video()
	isvideo = False #is the current item an image or video?
	connected = False #is the user connected to the interwebs?
api = API()
	
	
		
		
