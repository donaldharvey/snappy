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

if gtk.pygtk_version < (2,10,0):
	print "PyGtk 2.10.0 or later required"
	raise SystemExit

supports_alpha = False
win = None

#Rect-selection mumbo jumbo
class SelectArea(gtk.Window):
	escaped = False
	rect_selection = gtk.gdk.Rectangle(0, 0, 0, 0)
	def getselection(self, point):
		if not point:
			return (self.rectselection.x, self.rect_selection.y, self.rect_selection.width, self.rect_selection.height)
		elif point == 'x':
			return self.rect_selection.x
		elif point == 'y':
			return self.rect_selection.y
		elif point == 'width':
			return self.rect_selection.width
		elif point == 'height':
			return self.rect_selection.height

	def keypress(self, widget, event):
		global win
		if event.keyval == 65307:
			win.destroy()
			gtk.main_quit()
			self.escaped == True
	def clicked(self, widget, event):
		global mousedownlocation
		mousedownlocation = (event.x_root, event.y_root)
		print mousedownlocation
	
	def mousemove(self, widget, event):
		global win
		global mouselocation
		mouselocation = (event.x_root, event.y_root)
		if mouselocation [0] > mousedownlocation[0]:
			width = mouselocation[0] - mousedownlocation[0]
			x = mousedownlocation[0]
		else:
			width = mousedownlocation[0] - mouselocation[0]
			x = mouselocation[0]

		if mouselocation[1] > mousedownlocation[1]:
			height = mouselocation[1] - mousedownlocation[1]
			y = mousedownlocation[1]
		else:
			height = mousedownlocation[1] - mouselocation[1]
			y = mouselocation[1]
		global rect1
		global rect2
		global rect3
		global rect4
		x = int(x)
		y = int(y)
		width = int(width)
		height = int(height)
		(winwidth, winheight) = widget.get_size()
		self.rect_selection = gtk.gdk.Rectangle(x, y, width, height)
		rect1 = gtk.gdk.Rectangle(0, 0, winwidth, y)
		rect2 = gtk.gdk.Rectangle(0, y, x, height)
		rect3 = gtk.gdk.Rectangle(x + width, y, winwidth - (x + width), height)
		rect4 = gtk.gdk.Rectangle(0, y + height, winwidth, winheight - (y + height))
		win.queue_draw()
	def released(self, widget, event):
		global win
		global mouseuplocation
		mouseuplocation = (event.x_root, event.y_root)
		print mouseuplocation
		if mouseuplocation [0] > mousedownlocation[0]:
			width = mouseuplocation[0] - mousedownlocation[0]
			x = mousedownlocation[0]
		else:
			width = mousedownlocation[0] - mouseuplocation[0]
			x = mouseuplocation[0]

		if mouseuplocation[1] > mousedownlocation[1]:
			height = mouseuplocation[1] - mousedownlocation[1]
			y = mousedownlocation[1]
		else:
			height = mousedownlocation[1] - mouseuplocation[1]
			y = mouseuplocation[1]
		global rect1
		global rect2
		global rect3
		global rect4
		x = int(x)
		y = int(y)
		width = int(width)
		height = int(height)
		(winwidth, winheight) = widget.get_size()
		self.rect_selection = gtk.gdk.Rectangle(x, y, width, height)
		rect1 = gtk.gdk.Rectangle(0, 0, winwidth, y)
		rect2 = gtk.gdk.Rectangle(0, y, x, height)
		rect3 = gtk.gdk.Rectangle(x + width, y, winwidth - (x + width), height)
		rect4 = gtk.gdk.Rectangle(0, y + height, winwidth, winheight - (y + height))
		#This is the important bit - calls the drawing function below.
		win.queue_draw()
		win.destroy()
		gtk.main_quit()
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

		#this is the code to draw the selection box.
		cr.set_source_rgba(1, 1, 1, 0)
		cr.set_line_width(2)
		cr.rectangle(float(self.rect_selection.x), float(self.rect_selection.y), float(self.rect_selection.width), float(self.rect_selection.height))

		cr.fill()
		dashes = [ 1.0, 2.0 ]
		cr.set_source_rgba(1, 0.9, 0, 1)
		cr.set_line_width(2)
		cr.move_to(float(self.rect_selection.x), float(self.rect_selection.y))
		cr.line_to(float(self.rect_selection.x + self.rect_selection.width), float(self.rect_selection.y))
		cr.line_to(float(self.rect_selection.x + self.rect_selection.width), float(self.rect_selection.y + self.rect_selection.height))
		cr.line_to(float(self.rect_selection.x), float(self.rect_selection.y + self.rect_selection.height))
		cr.close_path()
		cr.stroke()

		if self.rect_selection.width > 0:
			pg = pangocairo.CairoContext(cr)
			pgl = pg.create_layout()
			pgfont = pango.FontDescription("sans bold 10")
			pgfont.set_family("Helvetica")
			pgl.set_text(str(self.rect_selection.width) + 'px x ' + str(self.rect_selection.height) + 'px')
			pgl.set_font_description(pgfont)
			cr.move_to(float(self.rect_selection.x), float(self.rect_selection.y + self.rect_selection.height))
			pg.show_layout(pgl)
		#This is of no importance ATM :P
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
	def __init__(self):
		global win

		win = gtk.Window()
		gtk.Window.__init__(self)
		win.set_property("skip-taskbar-hint", True)
		win.set_title('PyCairoShape clock')

		win.connect('delete-event', gtk.main_quit)

		win.set_app_paintable(True)
		win.set_double_buffered(False)

		win.connect('expose-event', self.expose)
		win.fullscreen()
		win.set_decorated(False)
		win.add_events(gdk.BUTTON_PRESS_MASK)
		win.add_events(gdk.BUTTON_RELEASE_MASK)
		win.add_events(gdk.BUTTON1_MOTION_MASK)
		win.add_events(gdk.KEY_RELEASE_MASK)
		self.screen_changed(win)
		win.connect('button-press-event', self.clicked)
		win.connect('button-release-event', self.released)
		win.connect_object('button-release-event', self.destroy, win)
		win.connect('motion-notify-event', self.mousemove)
		win.connect('realize', self.realize)
		win.connect('key_release_event', self.keypress)
		win.show_all()
		pass
	def main(self):
		gtk.main()
		return True
if __name__ == '__main__':
	screenshot = SelectArea()
	screenshot.main()
