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
from tesql.disk.formats.plain.objects import StringObject


class TestStringObject (TestCase):

    def setUp (self):
        self.fileobj = StringIO()

    def test_write_empty (self):
        obj = make_object('Key0', '')
        StringObject().write(obj, self.fileobj)

        self.assertEqual(self.fileobj.getvalue(), 'Key0: \n')

    def test_write_object_empty (self):
        obj = make_object('Key0', '')
        StringObject().write(obj, self.fileobj)

        self.assertEqual(self.fileobj.getvalue(), 'Key0: \n')

    def test_read_empty (self):
        obj = make_object('Key0', '')
        StringObject().write(obj, self.fileobj)
        self.fileobj.seek(0)

        nobj = StringObject().read(self.fileobj)

        self.assertEqual(obj, nobj)

    def test_read_object_empty (self):
        obj = make_object('Key0', '')
        StringObject().write(obj, self.fileobj)
        self.fileobj.seek(0)

        nobj = read_object(self.fileobj)

        self.assertEqual(obj, nobj)

    def test_write_simple (self):
        obj = make_object('Key1', 'Simple Text')
        StringObject().write(obj, self.fileobj)

        self.assertEqual(self.fileobj.getvalue(), 'Key1: Simple Text\n')

    def test_write_object_simple (self):
        obj = make_object('Key1', 'Simple Text')
        write_object(obj, self.fileobj)

        self.assertEqual(self.fileobj.getvalue(), 'Key1: Simple Text\n')

    def test_read_simple (self):
        obj = make_object('Key1', 'Simple Text')
        write_object(obj, self.fileobj)
        self.fileobj.seek(0)

        nobj = StringObject().read(self.fileobj)

        self.assertEqual(obj, nobj)

    def test_read_object_simple (self):
        obj = make_object('Key1', 'Simple Text')
        write_object(obj, self.fileobj)
        self.fileobj.seek(0)

        nobj = read_object(self.fileobj)

        self.assertEqual(obj, nobj)

    def test_write_multiline (self):
        obj = make_object('Key2', 'MultiLine text\nSecondLine')
        StringObject().write(obj, self.fileobj)

        self.assertEqual(self.fileobj.getvalue(),
                         'Key2: MultiLine text\n SecondLine\n')

    def test_write_object_multiline (self):
        obj = make_object('Key2', 'MultiLine text\nSecondLine')
        write_object(obj, self.fileobj)

        self.assertEqual(self.fileobj.getvalue(),
                         'Key2: MultiLine text\n SecondLine\n')

    def test_read_multiline (self):
        obj = make_object('Key2', 'MultiLine text\nSecondLine')
        write_object(obj, self.fileobj)
        self.fileobj.seek(0)

        nobj = StringObject().read(self.fileobj)

        self.assertEqual(obj, nobj)

    def test_read_object_multiline (self):
        obj = make_object('Key2', 'MultiLine text\nSecondLine')
        write_object(obj, self.fileobj)
        self.fileobj.seek(0)

        nobj = read_object(self.fileobj)

        self.assertEqual(obj, nobj)

    def test_write_multiline_empty (self):
        obj = make_object('Key3', 'MultiLine\n\nw/ empty line')
        StringObject().write(obj, self.fileobj)

        self.assertEqual(self.fileobj.getvalue(),
                         'Key3: MultiLine\n .\n w/ empty line\n')

    def test_write_object_multiline_empty (self):
        obj = make_object('Key3', 'MultiLine\n\nw/ empty line')
        write_object(obj, self.fileobj)

        self.assertEqual(self.fileobj.getvalue(),
                         'Key3: MultiLine\n .\n w/ empty line\n')

    def test_read_multiline_empty (self):
        obj = make_object('Key3', 'MultiLine\n\nw/ empty line')
        write_object(obj, self.fileobj)
        self.fileobj.seek(0)

        nobj = StringObject().read(self.fileobj)

        self.assertEqual(obj, nobj)

    def test_read_object_multiline_empty (self):
        obj = make_object('Key3', 'MultiLine\n\nw/ empty line')
        write_object(obj, self.fileobj)
        self.fileobj.seek(0)

        nobj = read_object(self.fileobj)

        self.assertEqual(obj, nobj)
