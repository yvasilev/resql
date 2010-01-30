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


def make_object (name, value):
    try:
        return Dictionary(name, Dictionary.validate(value))
    except:
        pass

    try:
        return List(name, List.validate(value))
    except:
        pass

    try:
        return String(name, String.validate(value))
    except:
        pass

    raise TypeError("Unable to identify the type of '%s'" % value)


from base import BaseObject
from data import String
from sequence import List
from mapping import Dictionary


from tesql import __author__, __license__, __version__
