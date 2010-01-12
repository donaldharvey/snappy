import os
import sys
snappy_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(snappy_dir)
from snappy.ui import main as ui_main

def main(*args, **kwargs):
	paths = kwargs.get('paths', {
		'DATA_PATH': os.path.join(snappy_dir, 'resources'),
		'ICONS_PATH': os.path.join(snappy_dir, 'resources'),
	})
	from snappy.globals import PATHS
	PATHS.update(paths)
	return ui_main(*args, **kwargs)

if __name__ == '__main__':
	main(*sys.argv)
