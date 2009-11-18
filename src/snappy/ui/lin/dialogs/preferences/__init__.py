import os
import gtk
class Preferences(object):
	def __init__(self):
		self.callbacks = {
			'help': self.help,
			'close': self.destroy,
		}
		self.window = self._build_dialog()
		self.notebook = self.window.get_child().get_children()[0]
		self.add_settings_area('main_area.glade')
		self.window.show_all()

	def _build_dialog(self):
		location = os.path.join(os.path.dirname(__file__), 'preferences_dialog.glade')
		builder = gtk.Builder()
		builder.add_from_file(location)
		win = builder.get_object('prefs_window')
		builder.connect_signals(self.callbacks)
		del builder
		return win

	def main(self):
		gtk.main()

	def add_settings_area(self, location):
		os.path.join(os.path.dirname(__file__), location)
		builder = gtk.Builder()
		builder.add_from_file(location)
		area_name = location.split('.')[-2]
		area_module = __import__(area_name)
		area = builder.get_object(area_name)
		container = gtk.HBox()
		container.set_border_width(10)
		container.add(area)
		label = builder.get_object(area_name + '_label')
		builder.connect_signals(area_module.callbacks)
		container._builder = builder
		
		def get_widget_by_name(name):
			def iterate_children(widget, name):
				if widget.get_name() == name:
					return widget
				try:
					for w in widget.get_children():
						result = iterate_children(w, name)
						if result is not None:
							return result
						else:
							'Result was none. Continuing'
							continue
				except AttributeError as e:
					print e

			return iterate_children(container, name)

		container.get_widget_by_name = get_widget_by_name
		area_module.startup(container)
		self.notebook.append_page(container, label)

	def help(self, widget, data=None):
		print 'HELP ME!'
		pass

	def destroy(self, widget, data=None):
		print 'Destroying!'
		self.window.destroy()
		gtk.main_quit()


if __name__ == '__main__':
	p = Preferences()
	p.main()