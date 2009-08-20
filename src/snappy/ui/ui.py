from platform import system

def main(args):
	platform = system().lower()
	try:
		realMain = __import__('snappy.ui.%s.main' % platform[0:3], globals(), locals(), ['main'], -1)
	except ImportError:
		print "Looks like you're running a system which isn't yet supported by Snappy."
		print "Think there's been a mistake? Go to snappy.sourceforge.net and file a bug!"
	else:
		realMain = realMain.main(args)
		