import os
import gtk
from snappy.globals import PATHS
class PreferencesArea(gtk.Alignment):
	def __init__(self):
		super(PreferencesArea, self).__init__()
		self.set_padding(10, 10, 10, 10)

	def get_widget_by_name(self, name):
		def iterate_children(widget, name):
			if widget.get_name() == name:
				return widget
			try:
				for w in widget.get_children():
					result = iterate_children(w, name)
					if result is not None:
						return result
					else:
						continue
			except AttributeError:
				pass
		return iterate_children(self, name)

class Preferences(object):
	def __init__(self):
		self.callbacks = {
			'help': self.help,
			'close': self.destroy,
		}
		self.window = self._build_dialog()
		self.notebook = self.window.get_child().get_children()[0]
		self.add_settings_area('main_area.glade')
		self.add_settings_area('sharing.glade')
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.show_all()

	def _build_dialog(self):
		path = os.path.join(PATHS['DATA_PATH'], 'glade', 'preferences', 'preferences_dialog.glade')
		builder = gtk.Builder()
		builder.add_from_file(path)
		win = builder.get_object('prefs_window')
		builder.connect_signals(self.callbacks)
		del builder
		return win

	def main(self):
		gtk.main()

	def add_settings_area(self, location):
		path = os.path.join(PATHS['DATA_PATH'], 'glade', 'preferences', location)
		builder = gtk.Builder()
		builder.add_from_file(path)
		area_name = location.split('.')[-2]
		area_module = getattr(__import__('snappy.ui.gtk.dialogs.preferences', fromlist=[area_name]), area_name)
		area = builder.get_object(area_name)
		container = self._get_tab_from_module(area_name, area_module)()
		container.add(area)
		container.startup()
		label = builder.get_object(area_name + '_label')
		builder.connect_signals(container)
		self.notebook.append_page(container, label)

	def help(self, widget, data=None):
		print 'HELP ME!'
		pass

	def _get_tab_from_module(self, name, area_module):
		for key, value in area_module.__dict__.iteritems():
			clean_name = name.replace('_', '').lower()
			if key.lower() == clean_name + 'tab':
				return value

	def destroy(self, widget, data=None):
		print 'Destroying!'
		self.window.destroy()
		gtk.main_quit()


if __name__ == '__main__':
	p = Preferences()
	p.main()