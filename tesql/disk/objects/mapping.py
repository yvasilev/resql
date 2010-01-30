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


class Dictionary (BaseObject):

    def __init__ (self, name, value):
        super(Dictionary, self).__init__(name, value)
        self.set_value(value)

    def __len__ (self):
        return len(self._values)

    def __getitem__ (self, key):
        return self._values[self._keys[key]]

    def __setitem__ (self, key, val):
        if key in self:
            self.replace(key, val)
        else:
            # Always append to the end of the Dictionary
            self._pos = len(self) - 1
            self.append(key, val)

    def __delitem__ (self, key):
        # FIXME: Implement
        pass

    def __contains__ (self, key):
        return key in self._keys

    def __eq__ (self, other):
        if isinstance(other, Dictionary):
            return self._values == other._values and \
                   self._keys == other._keys
        else:
            try:
                return dict(self) == other
            except:
                return False

    def __iter__ (self):
        return self.iterkeys()

    def select (self, key):
        self._pos = self._keys[key]

    @property
    def selected (self):
        if self._pos >= 0:
            return self._values[self._pos].name
        else:
            return None

    def prepend (self, key, val, select_new=True):
        if key in self:
            raise KeyError(key)

        obj = make_object(key, val)
        selkey = (select_new or self._pos < 0) and key or self.selected

        if isinstance(obj, Dictionary) and (self.selected and
           not isinstance(self[self.selected], Dictionary)):
            for i in xrange(len(self) - 1, -2, -1):
                if i == -1 or not isinstance(self._values[i], Dictionary):
                    self._values[i + 1:i + 1] = [obj]
                    for j in xrange(i + 1, len(self)):
                        self._keys[self._values[j].name] = j
                    break
        elif not isinstance(obj, Dictionary) and (self.selected and
           isinstance(self[self.selected], Dictionary)):
                self._values[0:0] = [obj]
                for i in xrange(0, len(self)):
                    self._keys[self._values[i].name] = i
        else:
            self._values[self._pos:self._pos] = [obj]

            for i in xrange(self._pos, len(self)):
                self._keys[self._values[i].name] = i

        self._pos = self._keys[selkey]

    def replace (self, key, val, select_new=True):
        self._values[self._keys[key]] = make_object(key, val)

        if select_new:
            self._pos = self._keys[key]

    def append (self, key, val, select_new=True):
        if key in self:
            raise KeyError(key)

        obj = make_object(key, val)
        selkey = (select_new or self._pos < 0) and key or self.selected

        if isinstance(obj, Dictionary) and (self.selected and
           not isinstance(self[self.selected], Dictionary)):
            self._values.append(obj)
            self._keys[key] = len(self) - 1
        elif not isinstance(obj, Dictionary) and (self.selected and
           isinstance(self[self.selected], Dictionary)):
            for i in xrange(len(self) - 1, -2, -1):
                if i == -1 or not isinstance(self._values[i], Dictionary):
                    self._values[i + 1:i + 1] = [obj]
                    for j in xrange(i + 1, len(self)):
                        self._keys[self._values[j].name] = j
                    break
        else:
            self._values[self._pos + 1:self._pos + 1] = [obj]
            for i in xrange(self._pos + 1, len(self)):
                self._keys[self._values[i].name] = i

        self._pos = self._keys[selkey]

    @staticmethod
    def validate (value):
        if not hasattr(value, 'iteritems'):
            raise TypeError('Value must be a mapping/dictionary')

        return value

    def set_value (self, value):
        value = self.validate(value)

        self._values = []
        self._keys = {}
        self._pos = -1

        for key, val in value.iteritems():
            self.append(key, val)

    def get_value (self):
        return self

    def keys (self):
        return list(self.iterkeys())

    def values (self):
        return list(self.itervalues())

    def items (self):
        return list(self.iteritems())

    def iterkeys (self):
        for item in self._values:
            yield item.name

    def itervalues (self):
        for item in self._values:
            yield item

    def iteritems (self):
        for item in self._values:
            yield (item.name, item)


from tesql import __author__, __license__, __version__
