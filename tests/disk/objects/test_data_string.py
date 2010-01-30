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

from tesql.disk.objects import String
from tesql.disk.objects import make_object


class TestString (TestCase):

    def test_init (self):
        s = String('Name', u'Value')

        self.assertEqual(s.name, 'Name')
        self.assertEqual(s.value, u'Value')

        s.set_value(u'New Value')

        self.assertEqual(s.value, u'New Value')

    def test_make_string (self):
        s = make_object('Name', u'Value')

        self.assertTrue(isinstance(s, String))
        self.assertEqual(s.name, 'Name')
        self.assertEqual(s.value, u'Value')

        s = make_object('Name', 'Value')

        self.assertTrue(isinstance(s, String))
        self.assertEqual(s.name, 'Name')
        self.assertEqual(s.value, u'Value')

    def test_eq (self):
        a = make_object('Name', 'Value')

        self.assertEqual(a, u'Value')
        self.assertNotEqual(a, u'Va1ue')

        b = make_object('Name', 'Value')
        c = make_object('Name', 'Va1ue')

        self.assertEqual(a, b)
        self.assertNotEqual(a, c)
