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


class String (BaseObject):

    def __init__ (self, name, value):
        super(String, self).__init__(name, value)
        self.set_value(value)

    def __contains__ (self, substr):
        """x.__contains__(y) <==> y in x"""

        return substr in self.value

    def __str__ (self):
        return self.value

    def __eq__ (self, other):
        if isinstance(other, String):
            return self.value == other.value
        else:
            return self.value == other

    @staticmethod
    def validate (value):
        if not hasattr(value, '__str__') or isinstance(value, type(None)):
            raise TypeError('Value must be a string')

        return unicode(value)

    def set_value (self, value):
        self._value = self.validate(value)

    def get_value (self):
        return self._value

    def encode (self, encoding='utf-8', errors='strict'):
        return self._value.encode(encoding, errors)

    def decode (self, encoding='utf-8', errors='strict'):
        return self._value.decode(encoding, errors)

    def split (self, sep=None, maxsplit=-1):
        """S.split([sep [,maxsplit]]) -> list of strings

        Return a list of the words in the string S, using sep as the
        delimiter string.  If maxsplit is given, at most maxsplit
        splits are done. If sep is not specified or is None, any
        whitespace string is a separator."""

        return self.value.split(sep, maxsplit)


from tesql import __author__, __license__, __version__
