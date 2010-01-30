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

from tesql.disk.objects import List
from tesql.disk.objects import make_object

class TestList (TestCase):

    def test_init_empty (self):
        l = List('Empty', [])

        self.assertEqual(l.name, 'Empty')
        self.assertEqual(list(l.value), [])
        self.assertEqual(l.value, [])

        self.assertEqual(len(l), 0)

    def test_init_strings (self):
        l = List('Text', ['Value1', 'Value2'])

        self.assertEqual(l.name, 'Text')
        self.assertEqual(list(l.value), ['Value1', 'Value2'])
        self.assertEqual(l.value, ['Value1', 'Value2'])

        self.assertEqual(len(l), 2)

        self.assertTrue('Value1' in l)
        self.assertTrue('Value2' in l)
        self.assertFalse('Value3' in l)

        self.assertEqual(l[0], 'Value1')
        self.assertEqual(l[1], 'Value2')
        self.assertRaises(IndexError, l.__getitem__, 2)

    def test_init_from_list (self):
        l = List('Text', ['Value1', 'Value2'])
        c = List('Name', l)

        self.assertEqual(c.name, 'Name')
        self.assertEqual(list(c.value), ['Value1', 'Value2'])
        self.assertEqual(c.value, ['Value1', 'Value2'])

        self.assertEqual(len(c), 2)

        self.assertTrue('Value1' in l)
        self.assertTrue('Value2' in l)
        self.assertFalse('Value3' in l)

        self.assertEqual(l[0], 'Value1')
        self.assertEqual(l[1], 'Value2')
        self.assertRaises(IndexError, l.__getitem__, 2)

        self.assertRaises(TypeError, List, 'Name', 'Value')

    def test_make_list (self):
        l = make_object('Empty', [])

        self.assertEqual(l.name, 'Empty')
        self.assertEqual(list(l.value), [])
        self.assertEqual(l.value, [])

        self.assertEqual(len(l), 0)

        l = make_object('Text', ['Value1', 'Value2'])

        self.assertEqual(l.name, 'Text')
        self.assertEqual(list(l.value), ['Value1', 'Value2'])
        self.assertEqual(l.value, ['Value1', 'Value2'])

        self.assertEqual(len(l), 2)

        self.assertTrue('Value1' in l)
        self.assertTrue('Value2' in l)
        self.assertFalse('Value3' in l)

        self.assertEqual(l[0], 'Value1')
        self.assertEqual(l[1], 'Value2')
        self.assertRaises(IndexError, l.__getitem__, 2)

        c = make_object('Name', l)

        self.assertEqual(c.name, 'Name')
        self.assertEqual(list(c.value), ['Value1', 'Value2'])
        self.assertEqual(c.value, ['Value1', 'Value2'])

        self.assertEqual(len(c), 2)

        self.assertTrue('Value1' in l)
        self.assertTrue('Value2' in l)
        self.assertFalse('Value3' in l)

        self.assertEqual(l[0], 'Value1')
        self.assertEqual(l[1], 'Value2')
        self.assertRaises(IndexError, l.__getitem__, 2)

    def test_eq (self):
        a = List('Text', [])
        a.append('Value1')
        a.append('Value2')

        self.assertEqual(a.name, 'Text')
        self.assertEqual(a, ['Value1', 'Value2'])
        self.assertEqual(list(a), ['Value1', 'Value2'])
        self.assertEqual(a.value, ['Value1', 'Value2'])
        self.assertEqual(list(a.value), ['Value1', 'Value2'])

        b = List('Text', {})
        b.append('Value2')
        b.append('Value1')

        self.assertEqual(b.name, 'Text')
        self.assertEqual(b, ['Value2', 'Value1'])

        c = List('Name', a)

        self.assertEqual(c.name, 'Name')
        self.assertEqual(c, ['Value1', 'Value2'])
        self.assertEqual(c, list(a))

        self.assertEqual(a, c)
        self.assertNotEqual(a, b)
        self.assertNotEqual(c, b)

        self.assertNotEqual(a, list(b.value))
        self.assertNotEqual(a, list(b))

        self.assertNotEqual(a, tuple(a))
        self.assertNotEqual(a, 'String')
