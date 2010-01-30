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
from StringIO import StringIO

from tesql.disk.objects import make_object

from tesql.disk.formats.plain import write_object
from tesql.disk.formats.plain import read_object
from tesql.disk.formats.plain.objects import DictionaryObject


class TestDisctionaryObject (TestCase):

    def setUp (self):
        self.fileobj = StringIO()

    def test_write_empty_empty (self):
        obj = make_object('', {})
        DictionaryObject().write(obj, self.fileobj)

        self.assertEqual(self.fileobj.getvalue(), '\n')

    def test_write_object_empty_empty (self):
        obj = make_object('', {})
        write_object(obj, self.fileobj)

        self.assertEqual(self.fileobj.getvalue(), '\n')

    def test_read_empty_empty (self):
        obj = make_object('', {})
        write_object(obj, self.fileobj)
        self.fileobj.seek(0)

        nobj = DictionaryObject().read(self.fileobj)

        self.assertEqual(obj, nobj)

    def test_read_object_empty_empty (self):
        obj = make_object('', {})
        write_object(obj, self.fileobj)
        self.fileobj.seek(0)

        nobj = read_object(self.fileobj, as_dictionary=True)

        self.assertEqual(obj, nobj)

    def test_write_key_empty (self):
        obj = make_object('Section', {})
        DictionaryObject().write(obj, self.fileobj)

        self.assertEqual(self.fileobj.getvalue(), '\n[Section]\n\n')

    def test_write_object_key_empty (self):
        obj = make_object('Section', {})
        write_object(obj, self.fileobj)

        self.assertEqual(self.fileobj.getvalue(), '\n[Section]\n\n')

    def test_read_key_empty (self):
        obj = make_object('Section', {})
        write_object(obj, self.fileobj)
        self.fileobj.seek(0)

        nobj = DictionaryObject().read(self.fileobj)

        self.assertEqual(obj, nobj)

    def test_read_object_key_empty (self):
        obj = make_object('Section', {})
        write_object(obj, self.fileobj)
        self.fileobj.seek(0)

        nobj = read_object(self.fileobj)

        self.assertEqual(obj, nobj)

    def test_write_key_strings_simple (self):
        obj = make_object('Section', {})
        obj.append('Key1', 'Value1')
        obj.append('Key2', 'Value2')
        obj.append('Key3', 'Value3')
        DictionaryObject().write(obj, self.fileobj)

        self.assertEqual(self.fileobj.getvalue(),
            '\n[Section]\n\nKey1: Value1\nKey2: Value2\nKey3: Value3\n')

    def test_write_object_key_strings_simple (self):
        obj = make_object('Section', {})
        obj.append('Key1', 'Value1')
        obj.append('Key2', 'Value2')
        obj.append('Key3', 'Value3')
        write_object(obj, self.fileobj)

        self.assertEqual(self.fileobj.getvalue(),
            '\n[Section]\n\nKey1: Value1\nKey2: Value2\nKey3: Value3\n')

    def test_read_key_strings_simple (self):
        obj = make_object('Section', {})
        obj.append('Key1', 'Value1')
        obj.append('Key2', 'Value2')
        obj.append('Key3', 'Value3')
        write_object(obj, self.fileobj)
        self.fileobj.seek(0)

        nobj = DictionaryObject().read(self.fileobj)

        self.assertEqual(obj, nobj)

    def test_read_object_key_strings_simple (self):
        obj = make_object('Section', {})
        obj.append('Key1', 'Value1')
        obj.append('Key2', 'Value2')
        obj.append('Key3', 'Value3')
        write_object(obj, self.fileobj)
        self.fileobj.seek(0)

        nobj = read_object(self.fileobj)

        self.assertEqual(obj, nobj)

    def test_write_empty_strings_simple (self):
        obj = make_object('', {})
        obj.append('Key1', 'Value1')
        obj.append('Key2', 'Value2')
        obj.append('Key3', 'Value3')
        DictionaryObject().write(obj, self.fileobj)

        self.assertEqual(self.fileobj.getvalue(),
            '\nKey1: Value1\nKey2: Value2\nKey3: Value3\n')

    def test_write_object_empty_strings_simple (self):
        obj = make_object('', {})
        obj.append('Key1', 'Value1')
        obj.append('Key2', 'Value2')
        obj.append('Key3', 'Value3')
        write_object(obj, self.fileobj)

        self.assertEqual(self.fileobj.getvalue(),
            '\nKey1: Value1\nKey2: Value2\nKey3: Value3\n')

    def test_read_empty_strings_simple (self):
        obj = make_object('', {})
        obj.append('Key1', 'Value1')
        obj.append('Key2', 'Value2')
        obj.append('Key3', 'Value3')
        write_object(obj, self.fileobj)
        self.fileobj.seek(0)

        nobj = DictionaryObject().read(self.fileobj)

        self.assertEqual(obj, nobj)

    def test_read_object_empty_strings_simple (self):
        obj = make_object('', {})
        obj.append('Key1', 'Value1')
        obj.append('Key2', 'Value2')
        obj.append('Key3', 'Value3')
        write_object(obj, self.fileobj)
        self.fileobj.seek(0)

        nobj = read_object(self.fileobj, as_dictionary=True)

        self.assertEqual(obj, nobj)

    def test_write_key_nested (self):
        obj = make_object('Section', {})
        obj.append('Key1', 'Value1')
        obj.append('SubSection', make_object('SubSection', {}))
        obj.append('Key2', 'Value2')
        DictionaryObject().write(obj, self.fileobj)

        self.assertEqual(self.fileobj.getvalue(),
            '\n[Section]\n\nKey1: Value1\nKey2: Value2\n\n[Section.SubSection]\n\n')

        obj['SubSection'].append('SubKey1', 'SubValue1')
        self.fileobj.truncate(0)
        DictionaryObject().write(obj, self.fileobj)

        self.assertEqual(self.fileobj.getvalue(),
            '\n[Section]\n\nKey1: Value1\nKey2: Value2\n\n[Section.SubSection]\n\n'
            'SubKey1: SubValue1\n')
