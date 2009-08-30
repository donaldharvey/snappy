def main(args):
	from snappy.backends.filesystem.backend import filesystem
	
	backend = filesystem('linux')
	print backend