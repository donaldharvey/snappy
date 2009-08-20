#!/usr/bin/python
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) #dev only
print sys.path
from snappy.ui.ui import main
if not sys.argv:
	main()
else:
	main(sys.argv)