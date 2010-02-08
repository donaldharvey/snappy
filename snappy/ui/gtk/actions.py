from areaselect import SelectArea
from screenshot import ScreenshotManager
from snappy.backend.configmanagers import get_conf_manager
from snappy.backend.httpstorage import get_sharing_service_from_conf, SharingError
from snappy.backend.urlproviders import get_url_shortener_from_conf
from snappy.ui.gtk.statusicon import StatusIcon
from threading import Timer
import gtk
import gobject
import os
from snappy.globals import PATHS
from socket import setdefaulttimeout
from urllib2 import URLError
setdefaulttimeout(120)
notify = StatusIcon().notify # Makes it a bit easier to write
def _upload_file(filename):
	"""
	Upload the file `filename` to the configured sharing service, and shortens
	the URL with the configured URL shortener. Also copies the shortened URL
	to the clipboard, and runs the post upload hook (if there is one).
	"""
	configmanager = get_conf_manager()

	sharingservice = get_sharing_service_from_conf(configmanager)
	urlprovider = get_url_shortener_from_conf(configmanager)
	try:
		import pdb
		#pdb.set_trace()
		StatusIcon().statusicon.set_icon_from_file(os.path.join(PATHS['ICONS_PATH'], 'icon-uploading.png'))
		# Store the file online
		url = sharingservice.store(filename)
		print 'Saved to', url
	except Exception, e:
		if type(e) == SharingError:
			try:
				title = e.args[1]
			except IndexError:
				title = e.default_title
			notify(title, e.args[0])
		elif type(e) == URLError:
			notify('Connection error', 'You may be disconnected from the internet, or the server you are using may be down.')
		StatusIcon().statusicon.set_icon_from_file(os.path.join(PATHS['ICONS_PATH'], 'icon-uploadfailed.png'))
		timer = Timer(5, StatusIcon().reset_icon)
		timer.setDaemon(True)
		timer.start()
		return None
	try:
		# Get the short url
		shorturl = urlprovider.shorten(url)
	except Exception:
		shorturl = url

	# Finally, add it to the clipboard.
	clipboard = gtk.clipboard_get('CLIPBOARD')
	clipboard.set_text(shorturl)
	StatusIcon().statusicon.set_icon_from_file(os.path.join(PATHS['ICONS_PATH'], 'icon-uploadfinished.png'))
	timer = Timer(5, StatusIcon().reset_icon)
	timer.setDaemon(True)
	timer.start()

	# Run post-upload hook
	try:
		configmanager.post_upload_hook(shorturl)
	except Exception:
		pass
	return shorturl

def capture_area():
	'''
	Take a quick screenshot of an area on the screen, upload to an online
	storage provider and add a short url to the clipboard.
	'''
	# Get the area.
	selectarea = SelectArea()
	selectarea.main()
	# Save to a temp file.
	if selectarea.cancelled:
		return None
	return _upload_file(selectarea.filename)


def capture_window():
	filename = ScreenshotManager().grab_window()
	return _upload_file(filename)

def capture_screen():
	filename = ScreenshotManager()._save_pixbuf_to_file(
		ScreenshotManager().grab_fullscreen())
	return _upload_file(filename)