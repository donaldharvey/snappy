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

# TODO: FINISH REFACTORING!
# THIS CODE IS TERRIBLE!

import gobject
import pango
import pygtk
import pangocairo
pygtk.require('2.0')
import gtk
from gtk import gdk
import cairo
import math
import thread
from screenshot import ScreenshotManager

if gtk.pygtk_version < (2,10,0):
	print "PyGtk 2.10.0 or later required"
	raise SystemExit

def get_luminance(colour):
	assert type(colour) == gtk.gdk.Color
	parts = dict()
	parts['r'] = float(colour.red) / 65535
	parts['g'] = float(colour.green) / 65535
	parts['b'] = float(colour.blue) / 65535
	for k, v in parts.iteritems():
		if v <= 0.03928:
			v = v / 12.92
		else:
			v = ((v + 0.055) / 1.055) ** 2.4
		parts[k] = v
	print parts
	luminance = (
		0.2126 * parts['r'] + 0.7152 *
		parts['g'] + 0.0722 *
		parts['b']
	)
	return luminance

def compute_border_colour():
	settings = gtk.settings_get_default()
	color_scheme_string = settings.props.gtk_color_scheme
	for line in color_scheme_string.split('\n'):
		if 'selected_bg_color' in line:
			colour = gtk.gdk.color_parse(line.split(': ')[1])
			print colour
	try:
		luminance = get_luminance(colour)
		bg_luminance = get_luminance(gtk.gdk.color_parse('#444'))
		print 'Ratio:', (luminance + 0.05) / (bg_luminance + 0.05)
		if (luminance + 0.05) / (bg_luminance + 0.05) < 4:
			# contrast ratio too low.
			raise ValueError
	except (ValueError, NameError):
		colour = gtk.gdk.color_parse('#71c837')
	return colour


def rounded_rectangle(cr, x, y, w, h, radius_x=5, radius_y=5):
	"""Draw a rectangle with rounded corners according to radius_x and radius_y."""
	# Following code is from http://www.cairographics.org/cookbook/roundedrectangles/
	ARC_TO_BEZIER = 0.55228475
	if radius_x > w - radius_x:
		radius_x = w / 2
	if radius_y > h - radius_y:
		radius_y = h / 2

	#approximate (quite close) the arc using a bezier curve
	c1 = ARC_TO_BEZIER * radius_x
	c2 = ARC_TO_BEZIER * radius_y

	cr.new_path()
	cr.move_to( x + radius_x, y)
	cr.rel_line_to( w - 2 * radius_x, 0.0)
	cr.rel_curve_to( c1, 0.0, radius_x, c2, radius_x, radius_y)
	cr.rel_line_to( 0, h - 2 * radius_y)
	cr.rel_curve_to( 0.0, c2, c1 - radius_x, radius_y, -radius_x, radius_y)
	cr.rel_line_to( -w + 2 * radius_x, 0)
	cr.rel_curve_to( -c1, 0, -radius_x, -c2, -radius_x, -radius_y)
	cr.rel_line_to(0, -h + 2 * radius_y)
	cr.rel_curve_to(0.0, -c2, radius_x - c1, -radius_y, radius_x, -radius_y)
	cr.close_path()


class SelectArea(gtk.Window):
	'''
	The SelectArea window provides area selection to Snappy.
	'''
	def get_selection(self, point=False):
		if not point:
			return (self.rect_selection.x, self.rect_selection.y, self.rect_selection.width, self.rect_selection.height)
		elif point == 'x':
			return self.rect_selection.x
		elif point == 'y':
			return self.rect_selection.y
		elif point == 'width':
			return self.rect_selection.width
		elif point == 'height':
			return self.rect_selection.height

	def keydown(self, widget, event):
		name = gtk.gdk.keyval_name(event.keyval)
		if name == 'Shift_L' or name == 'Shift_R':
			self.keep_square = True

	def keyup(self, widget, event):
		name = gtk.gdk.keyval_name(event.keyval)
		if name == 'Escape':
			if self.rect_selection.width and self.rect_selection.height:
				self.rect_selection = gtk.gdk.Rectangle(0, 0, 0, 0)
				self.show_intro = True
				self.mousedownlocation = None
				self.queue_draw()
			else:
				# escape key pressed. Destroy the window
				self.cancelled = True
				self.hide_all()
				self.destroy_win()
				gtk.main_quit()
		elif name == 'Shift_L' or name == 'Shift_R':
			self.keep_square = False

	def clicked(self, widget, event):
		self.mousedownlocation = (event.x_root, event.y_root)
		print self.mousedownlocation

	def mousemove(self, widget, event):
		if self.mousedownlocation is None:
			return
		self.mouselocation = (event.x_root, event.y_root)
		mx = event.x_root
		my = event.y_root
		oldmx = self.mousedownlocation[0]
		oldmy = self.mousedownlocation[1]

		if my > oldmy:
			height = my - oldmy
			y = my - height
		else:
			height = oldmy - my
			y = my

		if mx > oldmx:
			width = mx - oldmx
			x = mx - width
		else:
			width = oldmx - mx
			x = mx
			if self.keep_square:
				x = oldmx - height


		x = int(x)
		y = int(y)
		if self.keep_square:
			width = height
		width = int(width)
		height = int(height)
		self.rect_selection = gtk.gdk.Rectangle(x, y, width, height)
		self.queue_draw()

	def released(self, widget, event):
		if not (self.rect_selection.width and self.rect_selection.height):
			return
		self._is_finished = True
		self.queue_draw()
		#self.hide_all()
		#self.destroy_win()
		#gtk.main_quit()
		cropped_pixbuf = self.pixbuf.subpixbuf(self.rect_selection.x,
			self.rect_selection.y, self.rect_selection.width,
			self.rect_selection.height)
		self.filename = ScreenshotManager()._save_pixbuf_to_tempfile(cropped_pixbuf)
		print self.filename
		self.hide_all()
		self.destroy_win()
		gtk.main_quit()


	def draw(self, widget, event):
		'''Main drawing function.'''
		width = widget.get_allocation().width
		height = widget.get_allocation().height
		s = self.rect_selection
		widget.window.draw_pixbuf(None, self.pixbuf, 0, 0, 0, 0, -1, -1)

		# Get a cairo context
		cr = widget.window.cairo_create()


		# Make the window transparent
		#if self.supports_alpha == True:
		#	cr.set_source_rgba(0.0, 0.0, 0.0, 0)
		#else:
		#	cr.set_source_rgb(1.0, 1.0, 1.0)

		if not self._is_finished:
			# Draw the overlay at 75% opacity
			cr.set_source_rgba(0, 0, 0, 0.75)
			#cr.rectangle(0, 0, float(width), float(height))
			#cr.mask(pat)

			# Draw the selection box
			#cr.rectangle(float(self.rect_selection.x), float(self.rect_selection.y), float(self.rect_selection.width), float(self.rect_selection.height))
			cr.rectangle(0, 0, s.x, height) # left panel
			cr.rectangle(s.x + s.width, 0, width - (s.x + s.width), height) # right panel
			cr.rectangle(0, 0, width, s.y) # top panel
			cr.rectangle(0, s.y + s.height, width, height - (s.y + s.height)) # bottom panel
			cr.fill()
			cr.stroke()

		cr.fill()

		if self.show_intro:
			# Draw the text telling the user what to do.
			self.pg = pangocairo.CairoContext(cr)
			# Check if the pango layout for the intro text exists,
			# if not create it and add necessary attributes
			try:
				self.pgl_intro
			except AttributeError:
				self.pgl_intro = self.pg.create_layout()
				pgfont = pango.FontDescription("sans bold 18")
				pgfont.set_family("MgOpen Moderna")
				self.pgl_intro.set_markup('Drag the mouse to select an area to capture, or press the Escape key to cancel.')
				self.pgl_intro.set_font_description(pgfont)

			(pglw, pglh) = self.pgl_intro.get_pixel_size()
			cr.set_source_rgba(0.1, 0.1, 0.1, self.intro_opacity)
			padding = (25, 20)
			self.pgl_intro.set_width((width - padding[0]) * pango.SCALE)
			rounded_rectangle(
				cr,
				(width / 2) - ((pglw + padding[0]) / 2),
				(height / 2) - ((pglh + padding[1]) / 2),
				pglw + padding[0],
				pglh + padding[1],
				5,
				5
			)
			cr.fill()

			cr.set_source_rgba(1, 1, 1, self.intro_opacity)
			step = 0.05

			# Fade the intro text in or out.
			if self.rect_selection.height and self.rect_selection.width:
				if self.intro_opacity > step:
					self.intro_opacity -= step
				else:
					self.intro_opacity = 0.00
					self.show_intro = False
			else:
				if 1 - self.intro_opacity > step:
					self.intro_opacity += step
				else:
					self.intro_opacity = 1.00
					self.show_intro

			pglx = (width / 2) - (pglw / 2)
			pgly = (height / 2) - (pglh / 2)
			cr.move_to(pglx, pgly)
			self.pg.show_layout(self.pgl_intro)

		if not self._is_finished and (self.rect_selection.x > 0 or self.rect_selection.y > 0):
			cr.set_source_rgba(self.border_colour_r, self.border_colour_g, self.border_colour_b, 1)
			cr.set_line_width(2)
			cr.move_to(s.x, s.y)
			cr.line_to(s.x + s.width, s.y)
			cr.line_to(s.x + s.width, s.y + s.height)
			cr.line_to(s.x, s.y + s.height)
			cr.close_path()
			cr.stroke()

			self.pg = pangocairo.CairoContext(cr)
			try:
				self.pgl_area_text
			except AttributeError:
				self.pgl_area_text = self.pg.create_layout()
				pgfont = pango.FontDescription("sans bold 12")
				pgfont.set_family("MgOpen Moderna")
				self.pgl_area_text.set_font_description(pgfont)

			self.pgl_area_text.set_markup(str(self.rect_selection.width) + 'px x ' + str(self.rect_selection.height) + 'px\n<span size="small">Hold Shift for square, or press Escape to start again.</span>')
			(pglw, pglh) = self.pgl_area_text.get_pixel_size()
			#print 'Pango layout width, height: ' + str(pglw + self.rect_selection.width) + ', ' + str(pglh + self.rect_selection.height)
			pglx = float(s.x)
			pgly = float(s.height + s.y)

			#print width, height
			cr.move_to(pglx, pgly)
			self.pg.show_layout(self.pgl_area_text)
		if self.show_intro:
			self.queue_draw()
		return False

	def destroy_win(self, widget=None, data=None):
		gtk.main_quit()

	def screen_changed(self, widget=None, old_screen=None):
		screen = self.get_screen()
		colormap = screen.get_rgba_colormap()
		if colormap == None:
			print 'Your screen does not support alpha channels!'
			colormap = screen.get_rgb_colormap()
			self.supports_alpha = False
		else:
			print 'Your screen supports alpha channels!'
			self.supports_alpha = True

		self.set_colormap(colormap)

		return True

	def realize(self, widget):
		cursor = gtk.gdk.Cursor(gtk.gdk.CROSSHAIR)
		widget.window.set_cursor(cursor)


	def __init__(self):
		self.cancelled = False
		self.rect_selection = gtk.gdk.Rectangle(0, 0, 0, 0)
		self._is_finished = False
		self.keep_square = False
		self.intro_opacity = 1.0
		self.show_intro = True
		self.pixbuf = ScreenshotManager().grab_fullscreen()
		gtk.Window.__init__(self)
		area = gtk.DrawingArea()
		self.add(area)
		border_colour = compute_border_colour()
		print border_colour
		self.border_colour_r = float(border_colour.red) / 65535
		self.border_colour_g = float(border_colour.green) / 65535
		self.border_colour_b = float(border_colour.blue) / 65535
		print self.border_colour_b
		self.set_property("skip-taskbar-hint", True)
		self.set_keep_above(True)
		self.connect('delete-event', gtk.main_quit)

		self.set_app_paintable(True)
		self.set_double_buffered(False)

		area.connect('expose-event', self.draw)
		self.fullscreen()
		self.set_decorated(False)
		self.add_events(gdk.BUTTON_PRESS_MASK)
		self.add_events(gdk.BUTTON_RELEASE_MASK)
		self.add_events(gdk.BUTTON1_MOTION_MASK)
		self.add_events(gdk.KEY_RELEASE_MASK)
		self.screen_changed()
		self.connect('button-press-event', self.clicked)
		self.connect('button-release-event', self.released)
		#self.connect_object('button-release-event', self.destroy_win, self)
		self.connect('motion-notify-event', self.mousemove)
		self.connect('realize', self.realize)
		self.connect('key_press_event', self.keydown)
		self.connect('key_release_event', self.keyup)
		self.show_all()
		pass

	def main(self):
		gtk.main()

if __name__ == '__main__':
	screenshot = SelectArea()
	screenshot.main()
