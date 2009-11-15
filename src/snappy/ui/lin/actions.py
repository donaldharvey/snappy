from areaselect import SelectArea
from screenshot import screenshotmanager
import gtk
def quickshot():
	'''
	Take a quick screenshot of an area on the screen, upload to an online
	storage provider and add a short url to the clipboard.
	'''
	# Get the required area.
	selectarea = SelectArea()
	selectarea.main()
	# Save to a temp file.
	filename = selectarea.filename

	from snappy.backend.configmanagers import get_conf_manager
	configmanager = get_conf_manager()
	# Get the FTP storage backend for now.
	# Later, get an appropriate HttpStorage provider from the conf manager.
	from snappy.backend.httpstorage.ftpstorage import FtpStorage as HttpStorage
	httpstorage = HttpStorage(configmanager)

	# TODO: Get a UrlProvider from the ConfigManager.
	from snappy.backend.urlproviders.trim import TrimUrlProvider as UrlProvider
	urlprovider = UrlProvider()

	# Store the file online
	url = httpstorage.store(filename)
	print 'Saved to', url

	# Get the short url
	shorturl = urlprovider.shorten(url)

	# Finally, add it to the clipboard.
	clipboard = gtk.clipboard_get('CLIPBOARD')
	clipboard.set_text(shorturl)
	return shorturl
