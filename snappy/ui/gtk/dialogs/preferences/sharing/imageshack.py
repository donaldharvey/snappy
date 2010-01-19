from snappy.ui.gtk.dialogs.preferences.sharing import SharingWindow
from snappy.backend.configmanagers import get_conf_manager
conf_manager = get_conf_manager()

class ImageShackWindow(SharingWindow):
	def startup(self):
		pass


	def ok(self, widget, data=None):
		self.close()