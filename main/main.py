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

## Imports:
## TODO: Check for and implement gConf

import pygtk
pygtk.require('2.0')
import gtk
import pynotify
import os, sys
sys.path.append('../..')
import time as ttime
from snappy.main.config import *
from snappy.main.areaselect import SelectArea
from snappy.main.actions import Actions
from snappy.main.api import api
from snappy.main.screenshot import Screenshot
from snappy.main.statusicon import StatusIcon
if sys.platform == 'win32':
	api.os = 'Windows'
elif sys.platform == 'darwin':
	api.os = 'Mac OS X'
else:
	api.os = 'Unix'
	


## End Imports
#def FTPupload(filename, path):
#	try:
#		ftp = FTP(ftpserver) ftp.login(ftpusername,ftppassword)
#		ftp.cwd(ftpdirectory) file = open(path) ftp.storbinary("STOR " +
#		filename, file) ftp.quit() file.close() url = ftpserver + '/' +
#		ftpdirectory + '/' + filename
#	except:
#		print sys.exc_info()
#	else:
#		print "Successfully uploaded " + filename + "." return url

		#if url:
		#	#Epic pynotify stuff.
		#	pynotify.init("PySnap")
		#	notification = pynotify.Notification("Screenshot saved to " + url, "Epic win! Screenshot saved in the temp folder... but--oh my!--this message is about to self destruct!", "dialog-warning")
		#	notification.set_urgency(pynotify.URGENCY_NORMAL)
		#	notification.set_timeout(10000)
		#	notification.attach_to_status_icon(statusicon)
		#	notification.show()

		#	clipboard = gtk.clipboard_get("CLIPBOARD")
		#	clipboard.set_text(url)

class screenshotWin:
	def popup(self, widget, button, time, data=None):
		if button == 3:
			if data:
				data.show_all()
				data.popup(None, None, None, 3, time)
		pass

# Show_Hide callback
	def show_hide(self, widget,response_id, data= None):
		if response_id == gtk.RESPONSE_YES:
				widget.hide()
		else:
				widget.hide()

	# destroy callback
	def destroy(widget, data=None):
		gtk.main_quit()


	def __init__(self):
		#builder = gtk.Builder()
		#builder.add_from_file("settings.xml")
		statusicon = StatusIcon()
		statusicon.main()
		
	def main(self):
		gtk.main()
		

print __name__



if __name__ == "__main__":
	screenshotwin = screenshotWin()
	screenshotwin.main()




