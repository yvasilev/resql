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

from tesql.disk.objects import Dictionary
from tesql.disk.objects import make_object


class TestDisctionary (TestCase):

    def test_init_empty (self):
        d = Dictionary('Empty', {})

        self.assertEqual(d.name, 'Empty')
        self.assertEqual(dict(d.value), {})
        self.assertEqual(d.value, {})

        self.assertEqual(len(d), 0)

    def test_init_strings (self):
        d = Dictionary('Text', {'Key1': 'Value1', 'Key2': 'Value2'})

        self.assertEqual(d.name, 'Text')
        self.assertEqual(dict(d.value), {'Key1': 'Value1', 'Key2': 'Value2'})
        self.assertEqual(d.value, {'Key1': 'Value1', 'Key2': 'Value2'})

        self.assertEqual(len(d), 2)

        self.assertTrue('Key1' in d)
        self.assertTrue('Key2' in d)
        self.assertFalse('Key3' in d)

        self.assertEqual(d['Key1'], 'Value1')
        self.assertEqual(d['Key2'], 'Value2')
        self.assertRaises(KeyError, d.__getitem__, 'Key3')

    def test_init_from_dictionary (self):
        d = Dictionary('Text', {'Key1': 'Value1', 'Key2': 'Value2'})
        c = Dictionary('Name', d)

        self.assertEqual(c.name, 'Name')
        self.assertEqual(dict(c.value), {'Key1': u'Value1', 'Key2': u'Value2'})
        self.assertEqual(c.value, {'Key1': 'Value1', 'Key2': 'Value2'})

        self.assertEqual(len(c), 2)

        self.assertRaises(TypeError, Dictionary, 'Name', 'Value')

    def test_make_dictionary (self):
        d = make_object('Empty', {})

        self.assertEqual(d.name, 'Empty')
        self.assertEqual(dict(d.value), {})
        self.assertEqual(d.value, {})

        self.assertEqual(len(d), 0)

        d = make_object('Text', {'Key1': 'Value1', 'Key2': 'Value2'})

        self.assertEqual(d.name, 'Text')
        self.assertEqual(dict(d.value), {'Key1': 'Value1', 'Key2': 'Value2'})
        self.assertEqual(d.value, {'Key1': 'Value1', 'Key2': 'Value2'})

        self.assertEqual(len(d), 2)

        self.assertTrue('Key1' in d)
        self.assertTrue('Key2' in d)
        self.assertFalse('Key3' in d)

        self.assertEqual(d['Key1'], 'Value1')
        self.assertEqual(d['Key2'], 'Value2')
        self.assertRaises(KeyError, d.__getitem__, 'Key3')

        c = make_object('Name', d)

        self.assertEqual(c.name, 'Name')
        self.assertEqual(dict(c.value), {'Key1': u'Value1', 'Key2': u'Value2'})
        self.assertEqual(c.value, {'Key1': 'Value1', 'Key2': 'Value2'})

        self.assertRaises(TypeError, Dictionary, 'Name', 'Value')

        self.assertEqual(len(c), 2)

    def test_prepend (self):
        d = Dictionary('Empty', {})

        self.assertEqual(d, {})
        self.assertEqual(d.keys(), [])
        self.assertEqual(d.selected, None)

        d.prepend('Key4', 'Value4', select_new=False)

        self.assertEqual(d, {'Key4': 'Value4'})
        self.assertEqual(d.keys(), ['Key4'])
        self.assertEqual(d.selected, 'Key4')

        d.prepend('Key1', 'Value1', select_new=False)

        self.assertEqual(d, {'Key1': 'Value1', 'Key4': 'Value4'})
        self.assertEqual(d.keys(), ['Key1', 'Key4'])
        self.assertEqual(d.selected, 'Key4')

        d.prepend('Key2', 'Value2')

        self.assertEqual(d, {'Key1': 'Value1', 'Key2': 'Value2', 'Key4': 'Value4'})
        self.assertEqual(d.keys(), ['Key1', 'Key2', 'Key4'])
        self.assertEqual(d.selected, 'Key2')

        d.select('Key4')

        self.assertEqual(d.selected, 'Key4')

        d.prepend('Key3', 'Value3')

        self.assertEqual(d, {'Key1': 'Value1', 'Key2': 'Value2', 'Key3': 'Value3', 'Key4': 'Value4'})
        self.assertEqual(d.keys(), ['Key1', 'Key2', 'Key3', 'Key4'])
        self.assertEqual(d.selected, 'Key3')


        self.assertRaises(KeyError, d.prepend, 'Key1', 'Value1')

    def test_prepend_nested (self):
        d = Dictionary('Section1', {})
        d.prepend('Key2', 'Value2')

        self.assertEqual(d.keys(), ['Key2'])
        self.assertEqual(d.selected, 'Key2')

        d.prepend('Section3', {}, select_new=False)

        self.assertEqual(d.keys(), ['Key2', 'Section3'])
        self.assertEqual(d.selected, 'Key2')

        d.prepend('Section2', {})

        self.assertEqual(d.keys(), ['Key2', 'Section2', 'Section3'])
        self.assertEqual(d.selected, 'Section2')

        d.prepend('Key1', 'Value1')

        self.assertEqual(d.keys(), ['Key1', 'Key2', 'Section2', 'Section3'])
        self.assertEqual(d.selected, 'Key1')

    def test_append (self):
        d = Dictionary('Empty', {})

        self.assertEqual(d, {})
        self.assertEqual(d.keys(), [])
        self.assertEqual(d.selected, None)

        d.append('Key1', 'Value1', select_new=False)

        self.assertEqual(d, {'Key1': 'Value1'})
        self.assertEqual(d.keys(), ['Key1'])
        self.assertEqual(d.selected, 'Key1')

        d.append('Key3', 'Value3', select_new=False)

        self.assertEqual(d, {'Key1': 'Value1', 'Key3': 'Value3'})
        self.assertEqual(d.keys(), ['Key1', 'Key3'])
        self.assertEqual(d.selected, 'Key1')

        d.append('Key2', 'Value2')

        self.assertEqual(d, {'Key1': 'Value1', 'Key2': 'Value2', 'Key3': 'Value3'})
        self.assertEqual(d.keys(), ['Key1', 'Key2', 'Key3'])
        self.assertEqual(d.selected, 'Key2')

        d.select('Key3')

        self.assertEqual(d.selected, 'Key3')

        d.append('Key4', 'Value4')

        self.assertEqual(d, {'Key1': 'Value1', 'Key2': 'Value2', 'Key3': 'Value3', 'Key4': 'Value4'})
        self.assertEqual(d.keys(), ['Key1', 'Key2', 'Key3', 'Key4'])
        self.assertEqual(d.selected, 'Key4')

        self.assertRaises(KeyError, d.prepend, 'Key1', 'Value1')

    def test_append_nested (self):
        d = Dictionary('Section1', {})
        d.append('Key1', 'Value1')

        self.assertEqual(d.keys(), ['Key1'])
        self.assertEqual(d.selected, 'Key1')

        d.append('Section2', {}, select_new=False)

        self.assertEqual(d.keys(), ['Key1', 'Section2'])
        self.assertEqual(d.selected, 'Key1')

        d.append('Key2', 'Value2')

        self.assertEqual(d.keys(), ['Key1', 'Key2', 'Section2'])
        self.assertEqual(d.selected, 'Key2')

        d.append('Section3', {})

        self.assertEqual(d.keys(), ['Key1', 'Key2', 'Section2', 'Section3'])
        self.assertEqual(d.selected, 'Section3')

        d.append('Key3', 'Value3')

        self.assertEqual(d.keys(), ['Key1', 'Key2', 'Key3', 'Section2', 'Section3'])
        self.assertEqual(d.selected, 'Key3')

    def test_eq (self):
        a = Dictionary('Text', {})
        a.append('Key1', 'Value1')
        a.append('Key2', 'Value2')

        self.assertEqual(a.name, 'Text')
        self.assertEqual(a, {'Key1': 'Value1', 'Key2': 'Value2'})
        self.assertEqual(dict(a), {'Key1': 'Value1', 'Key2': 'Value2'})
        self.assertEqual(a.value, {'Key1': 'Value1', 'Key2': 'Value2'})
        self.assertEqual(dict(a.value), {'Key1': 'Value1', 'Key2': 'Value2'})

        b = Dictionary('Text', {})
        b.append('Key2', 'Value2')
        b.append('Key1', 'Value1')

        self.assertEqual(b.name, 'Text')
        self.assertEqual(b, {'Key2': 'Value2', 'Key1': 'Value1'})

        c = Dictionary('Name', a)

        self.assertEqual(c.name, 'Name')
        self.assertEqual(c, {'Key1': 'Value1', 'Key2': 'Value2'})
        self.assertEqual(c, dict(a))

        self.assertEqual(a, c)
        self.assertNotEqual(a, b)
        self.assertNotEqual(c, b)

        self.assertEqual(a, dict(b.value))
        self.assertEqual(a, dict(b))
