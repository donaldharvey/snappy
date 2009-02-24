#!/usr/bin/env python
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

#All imports we need
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
print sys.path
import gobject
import pango
import pygtk
import pangocairo
pygtk.require('2.0')
import gtk
from gtk import gdk
import cairo
from datetime import datetime
from snappy.main.config import enabledplugins
from snappy.main.api import API, api

if gtk.pygtk_version < (2,10,0):
	print "PyGtk 2.10.0 or later required"
	raise SystemExit

supports_alpha = False
win = None

class Actions(gtk.Window):
	escaped = False
	def keypress(self, widget, event):
		global win
		if event.keyval == 65307:
			win.destroy()
			gtk.main_quit()
			self.escaped == True
	def imageclick(self, widget, event, plugin):
			if event.button == 1:
				print 'Boo!'
				plugin.callback(plugin)
	#This is our main drawing function
	def image_area_expose(self, widget, event):
		img = cairo.ImageSurface.create_from_png(self.filename)
		imgwidth = img.get_width()
		imgheight = img.get_height()
		imgpat = cairo.SurfacePattern(img)
		cr = widget.window.cairo_create()
		(width, height) = widget.window.get_size()
		width = float(width)
		height = float(height)
		imgwidth = float(imgwidth)
		imgheight = float(imgheight)
		if imgwidth >= width or imgheight >= height:
			if width > height:
				scaleratio = imgwidth / width
			else:
				scaleratio = imgheight / height
			scaler = cairo.Matrix()
			scaler.scale(scaleratio, scaleratio)
			imgpat.set_matrix(scaler)
			imgpat.set_filter(cairo.FILTER_BEST)

			print scaleratio
		cr.set_source(imgpat)
		cr.paint()
		
	def expose(self, widget, event):
		global supports_alpha

		(width, height) = widget.get_size()

		#Get a cairo context
		cr = widget.window.cairo_create()

		#Make the window transparent
		if supports_alpha == True:
			cr.set_source_rgba(0.0, 0.0, 0.0, 0)
		else:
			cr.set_source_rgb(1.0, 1.0, 1.0) 
		cr.set_operator(cairo.OPERATOR_SOURCE)
		cr.paint()

		#And draw everything we want

		cr.set_source_rgba(0, 0, 0, 0.75)
		cr.rectangle(0, 0, float(width), float(height))
		#cr.mask(pat)
		cr.fill()
		cr.stroke()

		pm = gtk.gdk.Pixmap(None, width, height, 1)
		pmcr = pm.cairo_create()
		pmcr.rectangle(0, 0, float(width), float(height))
		pmcr.fill()
		pmcr.stroke()
		#Apply input mask
		win.input_shape_combine_mask(pm, 0, 0)

		return False

	def destroy(self, widget, data=None):
		gtk.main_quit()
		return 'failed!'


	def set_image_size(self, image):
		imagewidth = image.get_width()
		imageheight = image.get_height()
		screenheight = gtk.gdk.screen_height()
		screenwidth = gtk.gdk.screen_width()
		maxwidth = screenwidth - 20
		maxheight = screenheight - 110
		ratio = float(imagewidth) / float(imageheight)
		mustscale = False
		if imageheight >= maxheight:
			print 'hi - height = ' + str(imageheight)
			print ratio
			areaheight = maxheight
			mustscale = True
		if imagewidth >= maxwidth:
			print 'hi - width = ' + str(imagewidth)
			areawidth = maxwidth
			mustscale = True
			
		if mustscale:
			if ratio >= 1 and maxheight > imageheight: #Width > height in this case.
				areawidth = maxwidth
				areaheight = (1 / ratio) * maxwidth
			else:
				areawidth = ratio * maxheight
				areaheight = maxheight
		else:
			print "This doesn't have to scale!"
			print ratio
			print str(imagewidth) + ' x ' + str(imageheight)
			areawidth = imagewidth
			areaheight = imageheight
		print "It works"
		print (int(areawidth), int(areaheight))
		return int(areawidth), int(areaheight)
	def screen_changed(self, widget, old_screen=None):

		global supports_alpha

		screen = widget.get_screen()
		colormap = screen.get_rgba_colormap()
		if colormap == None:
			print 'Your screen does not support alpha channels!'
			colormap = screen.get_rgb_colormap()
			supports_alpha = False
		else:
			print 'Your screen supports alpha channels!'
			supports_alpha = True

		widget.set_colormap(colormap)

		return True


	def realize(self, widget):
		cursor = gtk.gdk.Cursor(gtk.gdk.CROSSHAIR)
		widget.window.set_cursor(cursor)
	
	#This is the main function. Basically it sets all the window properties and
	#hooks up all the events.
	def __init__(self, apiobject):
		self.filename = apiobject.path
		global win

		win = gtk.Window()
		gtk.Window.__init__(self)
		win.set_title('Snappy')

		win.connect('delete-event', gtk.main_quit)
		win.set_app_paintable(True)
		win.set_double_buffered(True)

		win.connect('expose-event', self.expose)
		win.fullscreen()
		win.set_decorated(False)
		self.screen_changed(win)
		win.connect('realize', self.realize)
		hbox = gtk.HBox(False, 0)
		vbox = gtk.VBox(False, 0)
		actionshbox = gtk.HBox(False, 0)
		actionshboxcontainer = gtk.HBox(False, 0)
		if not "video" in apiobject.mimetype:
			image = gtk.gdk.pixbuf_new_from_file(apiobject.path)
			apiobject.size = (image.get_width(), image.get_height)
			areawidth, areaheight = self.set_image_size(image)
			print 'This is not a video'
		else:
			#Code for handling videos goes here!
			pass
		imagearea = gtk.DrawingArea()
		imagearea.set_size_request(areawidth, areaheight)
		imagearea.connect("expose-event", self.image_area_expose)
		hbox.pack_start(imagearea, True, False, 0)
		
		
		vbox.pack_start(hbox, True, False, 0)
		vbox.pack_start(actionshboxcontainer, True, False, 0)
		actionshboxcontainer.pack_start(actionshbox, True, False, 0)
		
		for pluginname in enabledplugins:
			pluginmodule = 'snappy.plugins.' + pluginname + '.' + pluginname
			imageeventbox = gtk.EventBox()
			imageeventbox.set_visible_window(False)
			actionshbox.pack_start(imageeventbox, True, True, 4)
			try:
				exec('from ' + pluginmodule + ' import ' + pluginname + ' as plugin')
				print 'Imported ' + pluginname + ' plugin.'
				icon = gtk.Image()
				icon.set_from_file('../plugins/' + pluginname + '/' + plugin.icon)
				imageeventbox.add(icon)
				imageeventbox.connect('button-release-event', self.imageclick, plugin)
				print plugin.icon
				icon.show()
				imageeventbox.show()
			except ImportError:
				print 'No script in the ' + pluginname + ' directory.'
		win.add(vbox)
		imagearea.show()
		vbox.show()
		hbox.show()
		
		
		win.show_all()
		pass
	def main(self):
		gtk.main()
		return True
if __name__ == '__main__':
	api.image.filename = "Screenshot-3.png"
	api.image.path = "/home2/donald/Screenshot-3.png"
	api.image.mimetype = "image/png"
	api.image.filesize = os.path.getsize(api.image.path)
	actions = Actions(api.image)
	actions.main()


