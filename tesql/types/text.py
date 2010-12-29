# Copyright (C) 2010 - Yuri Vasilevski <yvasilev@gentoo.org>
#
#    This file is part of tesql.
#
#    tesql is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from tesql.query import Filter

from base import BaseSortable, exportedmethod

class String (BaseSortable):

    def __init__ (self, encoding=None, *args, **kw):
        super(String, self).__init__(*args, **kw)

        self._encoding = encoding

        self.set_data(u'')

    @exportedmethod
    def startswith (self, prefix):
        return Filter(lambda x: x.field_get(self.name).startswith(prefix))

    @exportedmethod
    def contains (self, other):
        return Filter(lambda x: other in x.field_get(self.name))

    @exportedmethod
    def endswith (self, suffix):
        return Filter(lambda x: x.field_get(self.name).endswith(suffix))


from tesql import __author__, __license__, __version__
