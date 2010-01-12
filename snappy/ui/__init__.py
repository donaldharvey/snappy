import sys
def main(*args, **kwargs):
	# right now there's only gtk available.
	# When more frontends have been coded, this file will detect the OS and use
	# the correct frontend
	from snappy.ui.gtk.main import main
	main(*args)
