from snappy.ui.gtk.dialogs.preferences.sharing import SharingWindow
from snappy.backend.configmanagers import get_conf_manager
conf_manager = get_conf_manager()
class FTPWindow(SharingWindow):
	def startup(self):
		self.data = {}
		for key, value in conf_manager['ftp.*'].iteritems():
			if key == 'use_sftp':
				self.get_widget_by_name(key).set_active(bool(int(value)))
			else:
				self.get_widget_by_name(key).set_text(value)

	def value_changed(self, widget, data=None):
		if widget.get_name() == 'use_sftp':
			self.data[widget.get_name()] = str(int(widget.get_active()))
		else:
			self.data[widget.get_name()] = widget.get_text()

	def ok(self, widget, data=None):
		for key, value in self.data.iteritems():
			conf_manager['ftp.%s' % key] = value
		self.close()