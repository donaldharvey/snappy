#!/usr/bin/env python
# Copyright (C) 2009 Donald S. F. Harvey
#
# This file is part of Snappy.
#
# Snappy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Snappy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Snappy.  If not, see <http://www.gnu.org/licenses/>.

class Backend():
	'''
	A dummy backend implementation which the real backends inherit from.
	Refer to this if building a new backend.
	'''
	
	requiresNetwork = False
	deps = () #List of strings representing distutils dependencies.
	class dbObject(object):
		def get(self, objtype, identifier):
			object = getattr(self, identifier)
			print 'Object %s with id %s' % (object, identifier)
			return object
			
		def set(self, objtype, object):
			'''
			Set an object. Object arg should be a tuple of its ID and its content.
			'''
			(identifier, content) = object
			setattr(self, identifier, content)
			print 'Object %s added' % identifier
			return identifier
		
		def delete(self, objtype, identifier):
			return identifier