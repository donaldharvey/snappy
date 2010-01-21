from snappy.ui.gtk.dialogs.preferences.sharing import SharingWindow
from snappy.backend.configmanagers import get_conf_manager
conf_manager = get_conf_manager()

class TinyPicWindow(SharingWindow):
	def startup(self):
		self.data = {}
		for key, value in conf_manager['tinypic.*'].iteritems():
			self.get_widget_by_name(key).set_text(value)
		self.get_widget_by_name('password').set_text(conf_manager.get_password('tinypic.password'))

	def value_changed(self, widget, data=None):
		self.data[widget.get_name()] = widget.get_text()

	def ok(self, widget, data=None):
		for key, value in self.data.iteritems():
			if key == 'password':
				conf_manager.set_password('tinypic.password', value)
			else:
				conf_manager['tinypic.%s' % key] = value
		self.close()