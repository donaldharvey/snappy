from areaselect import SelectArea
from screenshot import ScreenshotManager
from snappy.backend.configmanagers import get_conf_manager
from snappy.backend.httpstorage import get_sharing_service_from_conf
from snappy.backend.urlproviders import get_url_shortener_from_conf
import gtk

def _upload_file(filename):
	configmanager = get_conf_manager()

	sharingservice = get_sharing_service_from_conf(configmanager)
	urlprovider = get_url_shortener_from_conf(configmanager)

	# Store the file online
	url = sharingservice.store(filename)
	print 'Saved to', url

	# Get the short url
	shorturl = urlprovider.shorten(url)

	# Finally, add it to the clipboard.
	clipboard = gtk.clipboard_get('CLIPBOARD')
	clipboard.set_text(shorturl)

	return shorturl

def capture_area():
	'''
	Take a quick screenshot of an area on the screen, upload to an online
	storage provider and add a short url to the clipboard.
	'''
	# Get the required area.
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
	filename = ScreenshotManager()._save_pixbuf_to_tempfile(
		ScreenshotManager().grab_fullscreen())
	return _upload_file(filename)