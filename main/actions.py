#!/usr/bin/env python
#!/usr/bin/env python

#All imports we need
import sys
import gobject
import pango
import pygtk
import pangocairo
pygtk.require('2.0')
import gtk
from gtk import gdk
import cairo
from datetime import datetime
import math

if gtk.pygtk_version < (2,10,0):
	print "PyGtk 2.10.0 or later required"
	raise SystemExit

#Yeah, globals. Warning: this code is messy
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
	#This is our main drawing function
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
	def __init__(self, filename):
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
		image = gtk.Image()
		image.set_from_file(filename)
		vbox.pack_start(image, True, False, 0)
		
		hbox.pack_start(vbox, True, False, 0)
		
		win.add(hbox)
		image.show()
		vbox.show()
		hbox.show()
		win.show_all()
		pass
	def main(self):
		gtk.main()
		return True
if __name__ == '__main__':
	actions = Actions('/home2/donald/Screenshot-3.png')
	actions.main()


