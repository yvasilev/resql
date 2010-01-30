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


class Filter (object):

    def __init__ (self, func):
        self._filter = func

    def __call__ (self, instance):
        return self._filter(instance)

    def __and__ (self, other):
        return Filter(lambda x: self._filter(x) and other._filter(x))

    def __or__ (self, other):
        return Filter(lambda x: self._filter(x) or other._filter(x))

    def __invert__ (self):
        return Filter(lambda x: not self._filter(x))


from tesql import __author__, __license__, __version__
