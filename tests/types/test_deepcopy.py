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

from tesql.types import *


class TestTypeDeepCopy (TestCase):

    def test_string_empty (self):
        s = String()
        d = s.clone()

        self.assertNotEqual(id(s), id(d))
        self.assertEqual(s._data, d._data)
        self.assertEqual(id(s._constraints), id(d._constraints))

        self.assertEqual(s.marshal(), d.marshal())

    def test_string_data (self):
        s = String()
        s.set_data('The string to be copied.')
        d = s.clone()

        self.assertNotEqual(id(s), id(d))
        self.assertEqual(s._data, d._data)
        self.assertEqual(id(s._constraints), id(d._constraints))

        self.assertEqual(s.marshal(), d.marshal())

    def test_integer_empty (self):
        s = Integer()
        d = s.clone()

        self.assertNotEqual(id(s), id(d))
        self.assertEqual(s._data, d._data)
        self.assertEqual(id(s._constraints), id(d._constraints))

        self.assertEqual(s.marshal(), d.marshal())

    def test_integer_data (self):
        s = Integer()
        s.set_data(777)
        d = s.clone()

        self.assertNotEqual(id(s), id(d))
        self.assertEqual(s._data, d._data)
        self.assertEqual(id(s._constraints), id(d._constraints))

        self.assertEqual(s.marshal(), d.marshal())

