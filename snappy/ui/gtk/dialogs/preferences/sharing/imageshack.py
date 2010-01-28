from snappy.ui.gtk.dialogs.preferences.sharing import SharingWindow
from snappy.backend.configmanagers import get_conf_manager
conf_manager = get_conf_manager()

class ImageShackWindow(SharingWindow):
	def startup(self):
		self.get_widget_by_name('email').set_text(conf_manager['imageshack.email'])
		self.get_widget_by_name('password').set_text(conf_manager.get_password('imageshack.password'))


	def ok(self, widget, data=None):
		conf_manager['imageshack.email'] = self.get_widget_by_name('email').get_text()
		conf_manager.set_password('imageshack.password', self.get_widget_by_name('password').get_text())
		self.close()