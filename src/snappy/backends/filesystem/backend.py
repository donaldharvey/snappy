from snappy.base.backends.backend import Backend
import os
class filesystem(Backend):
	deps = ('pysqlite')
	def getObject(self, type, identifier):
			