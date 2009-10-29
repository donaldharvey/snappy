from areaselect import SelectArea
from screenshot import screenshotmanager
def quickshot():
	'''
	Take a quick screenshot of an area on the screen, upload to an online
	storage provider and add a short url to the clipboard.
	'''
	# Get the required area.
	selectarea = SelectArea()
	selectarea.main()
	rect = SelectArea.get_selection()
	screenshotmanager.grab_area(*rect)
