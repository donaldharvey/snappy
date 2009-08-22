def main(args):
	from snappy.backends.filesystem.backend import filesystem
	backend = filesystem()
	print backend