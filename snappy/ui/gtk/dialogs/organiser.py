import pygtk
pygtk.require('2.0')
import gtk
from snappy.backend.storage.filesystem.backend import fsbackend
from snappy.ui.gtk.widgets.captures import CapturesArea
class OrganiserDialog():
	def _iterate_categories(self):
		# Get data from DB.
		query = self.backend.dbobject.model.Category.select()
		categories = list(query)
		print categories
		# Sort the categories.
		unsorted_dict = dict()
		tempsorted = list()
		for category in categories:
			unsorted_dict[category.id] = category
			if category.parent == 0:
				#top level!
				tempsorted.append(category)
				del unsorted_dict[category.id]
		# We've put all the top level categories in tempsorted. Now we'll sort the rest.
		while len(unsorted_dict) > 0:
			print tempsorted
			for cat_id, category in unsorted_dict.copy().iteritems():
				parentindex = -1
				for descendant in range(len(tempsorted)):
					if category.parent == tempsorted[descendant].id:
						parentindex = descendant
						break
					else:
						print category.parent, '!=', tempsorted[descendant].id
				if parentindex != -1:
					tempsorted.insert(parentindex + 1, category)
					print 'Added', category.name, 'to index.'
					del unsorted_dict[cat_id]
				else:
					pass
					#print 'Couldn\'t find %s\'s parent.' % category.name
		return tempsorted

	def _get_category_icon(self, iconstring):
		icon = gtk.icon_theme_get_default().load_icon("folder", gtk.ICON_SIZE_MENU, 0)
		return icon

	def _add_categories_to_store(self, store):
		def match_func(row, data):
			column, key = data # data is a tuple containing column number, key
			return row[column] == key

		def search(rows, func, data):
			if not rows: return None
			for row in rows:
				if func(row, data):
					return row
				result = search(row.iterchildren(), func, data)
				if result: return result
			return None

		categories = self._iterate_categories()
		for category in categories:
			if category.parent == 0:
				parent = None
			else:
				parentid = category.parent
				parent = search(store, match_func, (0, parentid))
				parent = parent.iter
			icon = self._get_category_icon(category.icon)
			store.append(parent, (category.id, category.name, icon))

	def _create_categories_treeview(self):
		self.captures_store = gtk.TreeStore(int, str, gtk.gdk.Pixbuf) #id, name, icon
		self._add_categories_to_store(self.captures_store)
		# Create a TreeViewColumn
		col = gtk.TreeViewColumn("Category")
		# Create a column cell to display text
		col_cell_text = gtk.CellRendererText()
		# Create a column cell to display an image
		col_cell_img = gtk.CellRendererPixbuf()
		# Add the cells to the column
		col.pack_start(col_cell_img, False)
		col.pack_start(col_cell_text, True)
		# Bind the text cell to column 1 of the tree's model
		col.add_attribute(col_cell_text, "text", 1)
		# Bind the image cell to column 2 of the tree's model
		col.add_attribute(col_cell_img, "pixbuf", 2)

		# Create the TreeView and set our data store as the model
		tree = gtk.TreeView(self.captures_store)
		# Append the columns to the TreeView
		tree.append_column(col)
		return tree

	def hello(self, widget, data=None):
		print 'Hello universe.'

	def __init__(self, backend = fsbackend):
		self.backend = backend
		self.window = gtk.Window()
		self.window.connect('delete_event', lambda w: self.window.hide())

		vbox = gtk.VBox()


		def get_main_menu(self):
			window = self.window
			accelgroup = gtk.AccelGroup()
			item_factory = gtk.ItemFactory(gtk.MenuBar, "<main>", accelgroup)
			item_factory.create_items(self.menu_items)
			window.add_accel_group(accelgroup)
			self.item_factory = item_factory
			return item_factory.get_widget("<main>")

		self.menu_items = (
			('/_File', 				None, None, 0, '<Branch>'),
			('/File/New', 			None, self.hello, 0, None),
			('/_Edit', 				None, None, 0, '<Branch>'),
			('/Edit/_Preferences',	None, self.hello, 0, None),
		)

		menubar = get_main_menu(self)
		vbox.pack_start(menubar, False, True, 0)

		hpane = gtk.HPaned()
		categories_view = self._create_categories_treeview()
		hpane.add1(categories_view)

		captures = CapturesArea()
		hpane.add2(captures)
		self.window.connect('configure_event', captures._configure_event)
		vbox.pack_start(hpane)

		self.window.add(vbox)

		self.window.show_all()
		self.window.show()
		# TODO: Add menubar XML

	def main(self):
		gtk.main()

if __name__ == '__main__':
	#print iterate_categories(None)
	organiser = OrganiserDialog()
	organiser.main()