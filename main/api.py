#!/usr/bin/env python
# Copyright (C) 2009 Donald S. F. Harvey
#
# This file is part of Snappy.
#
# Snappy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Snappy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Snappy.  If not, see <http://www.gnu.org/licenses/>.
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
	class Settings:
		class Plugin:
			pass
		pass #Add more items later.
	os = ""
api = API()
	
	
		
		
