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

from base import BaseObject

from tesql.disk.objects import make_object


class List (BaseObject):

    def __init__ (self, name, value):
        super(List, self).__init__(name, value)
        self.set_value(value)

    def __len__ (self):
        return len(self._values)

    def __getitem__ (self, index):
        return self._values.__getitem__(index)

    def __setitem__ (self, index, value):
        return self._values.__setitem__(index, item)

    def __delitem__ (self, index):
        return self._values.__delitem__(index)

    def __iter__ (self):
        for item in self._values:
            yield item

    def __contains__ (self, item):
        return self._values.__contains__(item)

    def __eq__ (self, other):
        if isinstance(other, List):
            return self._values == other._values
        else:
            try:
                return list(self) == other
            except:
                return False

    def append (self, val):
        self._values.append(val)

    @staticmethod
    def validate (value):
        if not hasattr(value, '__iter__'):
            raise TypeError('Value must be a sequence')

        return value

    def set_value (self, value):
        value = self.validate(value)

        self._values = []

        for val in iter(value):
            self.append(val)

    def get_value (self):
        return self


from tesql import __author__, __license__, __version__
