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

from unittest import TestCase

from tesql.disk.formats.plain import PLAIN_OBJECTS

from tesql.disk.formats.plain.objects import StringObject
from tesql.disk.formats.plain.objects import ListObject
from tesql.disk.formats.plain.objects import DictionaryObject


class TestPlainInit (TestCase):

    def test_PLAIN_OBJECTS (self):
        self.assertEqual(len(PLAIN_OBJECTS), 3)
        self.assertEqual(PLAIN_OBJECTS, [DictionaryObject, StringObject,
                                         ListObject])
