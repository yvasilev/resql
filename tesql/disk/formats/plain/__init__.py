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

import inspect


def write_object (obj, fileobj, prefix=''):
    for pobj in PLAIN_OBJECTS:
        if isinstance(obj, pobj().match_type):
            return pobj().write(obj, fileobj, prefix)


def read_object (fileobj, as_dictionary=False):
    if as_dictionary:
        return objects.DictionaryObject().read(fileobj)

    for line in fileobj:
        if not line.strip():
            continue

        for pobj in PLAIN_OBJECTS:
            match = pobj().match_re.match(line)
            if match and match.groups():
                return pobj().read(fileobj, match)


import objects

from base import BasePlainObject

PLAIN_OBJECTS = sorted([x[1] for x in
                        inspect.getmembers(objects, inspect.isclass) if
                        issubclass(x[1], BasePlainObject) and
                        hasattr(x[1], 'priority')],
                       lambda x, y: x().priority - y().priority, reverse=True)


from tesql import __author__, __license__, __version__
