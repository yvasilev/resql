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


class Integer (BaseSortable):

    def __init__ (self, *args, **kw):
        super(Integer, self).__init__(*args, **kw)

        self.set_data(0)

    @exportedmethod
    def __lt__ (self, other):
        return Filter(lambda x: x.field_get(self.name) < other)

    @exportedmethod
    def __le__ (self, other):
        return Filter(lambda x: x.field_get(self.name) <= other)

    @exportedmethod
    def __ge__ (self, other):
        return Filter(lambda x: x.field_get(self.name) >= other)

    @exportedmethod
    def __gt__ (self, other):
        return Filter(lambda x: x.field_get(self.name) > other)

    def unmarshal (self, value):
        return int(value.decode(self._incoding))


class Indexer (Integer):

    def __init__ (self, *args, **kw):
        super(Indexer, self).__init__(*args, **kw)

    def set_next (self, entity):
        res = entity.query.sort_by(entity.meta.pk.descending).one()
        self.set_data(res and res.pk + 1 or 0)


from tesql import __author__, __license__, __version__
