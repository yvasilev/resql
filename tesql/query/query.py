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

import tesql


class Query (object):

    def __init__ (self, entity, parent=None):
        self._entity = entity
        self._parent = parent

    def __iter__ (self):
        iterable = self.parent and self.parent or ((self.entity, pk) for \
                   pk in tesql.orm.Session.default.list_primary_keys(self.entity))
        for e, pk in iterable:
            yield (e, pk)

    def __contains__ (self, key):
        return any(e == key[0] and pk == key[1] for e, pk in self)

    @property
    def entity (self):
        return self._entity

    @property
    def parent (self):
        return self._parent

    def all (self):
        return list(tesql.orm.Session.default.get(e, pk) for e, pk in self)

    def range (self, start=None, stop=None, step=None):
        return self.all()[start:stop:step]

    def one (self):
        try:
            return (tesql.orm.Session.default.get(e, pk) for e, pk in self).next()
        except StopIteration:
            return None

    def get (self, pk):
        if (self.entity, pk) in self:
            return tesql.orm.Session.default.get(self.entity, pk)
        else:
            return None

    def filter_by (self, *functions):
        return FilteringQuery(self.entity, parent=self, filters=functions)

    def sort_by (self, *functions):
        return SortingQuery(self.entity, parent=self, sorters=functions)

class FilteringQuery (Query):

    def __init__ (self, entity, parent=None, filters=tuple()):
        super(FilteringQuery, self).__init__(entity, parent=parent)

        self._filters = filters

    def __iter__ (self):
        iterable = self.parent and self.parent or ((self.entity, pk) for \
                   pk in tesql.orm.Session.default.list_primary_keys(self.entity))
        for e, pk in iterable:
            if all(func(tesql.orm.Session.default.get(e, pk))
                    for func in self._filters):
                yield (e, pk)


class SortingQuery (Query):

    def __init__ (self, entity, parent=None, sorters=tuple()):
        super(SortingQuery, self).__init__(entity, parent=parent)

        self._sorters = sorters

    def __iter__ (self):
        iterable = self.parent and self.parent or ((self.entity, pk) for \
                   pk in tesql.orm.Session.default.list_primary_keys(self.entity))
        iterable = (tesql.orm.Session.default.get(e, pk) for e, pk in iterable)
        for sorter in reversed(self._sorters):
            iterable = sorted(iterable, sorter)
        iterable = ((type(x), x.pk) for x in iterable)
        for e, pk in iterable:
            yield (e, pk)


from tesql import __author__, __license__, __version__
