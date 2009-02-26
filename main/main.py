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
import sys
sys.path.append('../..')
import pygtk
pygtk.require('2.0')
import gtk
import pynotify
import os, sys
import time as ttime
from snappy.main.config import *
from snappy.main.areaselect import SelectArea
from snappy.main.actions import Actions
from snappy.main.api import api
from snappy.main.screenshot import Screenshot
print sys.path
## End Imports
def FTPupload(filename, path):
	try:
		ftp = FTP(ftpserver)
		ftp.login(ftpusername,ftppassword)
		ftp.cwd(ftpdirectory)
		file = open(path)
		ftp.storbinary("STOR " + filename, file)
		ftp.quit()
		file.close()
		url = ftpserver + '/' + ftpdirectory + '/' + filename
	except:
		print sys.exc_info()
	else:
		print "Successfully uploaded " + filename + "."
		return url

def takeScreenshot(self, statusicon):
	#print "The size of the window is %d x %d" % sz
	areaselect = SelectArea()
	areaselect.main()
	if not areaselect.escaped:
		ttime.sleep(2)
		screenshot = Screenshot()
		screenshot.grabArea(areaselect.getselection('x'), areaselect.getselection('y'), areaselect.getselection('width'), areaselect.getselection('height'))
		actions = Actions(api.image)
		actions.main()

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
	def  destroy(widget, data=None):
				gtk.main_quit()


	def __init__(self):
		#builder = gtk.Builder()
		#builder.add_from_file("settings.xml")


		self.statusicon = gtk.StatusIcon()
		self.statusicon.set_from_file("../resources/icon.png")
		menu = gtk.Menu()

		## Here be the menu item definitions.
		item_screenshot = gtk.MenuItem("Take screenshot")
		item_preferences = gtk.MenuItem("Preferences")
		item_exit = gtk.MenuItem("Exit")

		## Now we connect these to their handlers.
		item_screenshot.connect("activate", takeScreenshot, self.statusicon)
		#item_preferences.connect("activate", settingswindow) #This function doesn't exist yet!
		item_exit.connect_object("activate", self.destroy, menu)

		##And finally, add these to the menu.
		menu.append(item_screenshot)
		menu.append(item_preferences)
		menu.append(item_exit)

		item_screenshot.show()
		item_preferences.show()
		item_exit.show()

		menu.set_title('Popup example')
		self.statusicon.connect("popup_menu", self.popup, menu)
		self.statusicon.connect("activate", takeScreenshot, self.statusicon)
		self.statusicon.set_visible(True)
			
	def main(self):
		gtk.main()

print __name__



if __name__ == "__main__":
	screenshotwin = screenshotWin()
	screenshotwin.main()




