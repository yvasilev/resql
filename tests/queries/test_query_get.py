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

import os

from unittest import TestCase

from tesql.orm import *
from tesql.types import *

from tesql.query import Query

class TestQueryGet (TestCase):

    def setUp (self):
        self.path = '/tmp/test.tesqldb'
        Session.default.bind(self.path)
        Session.default.expunge()
        if os.path.lexists(self.path):  # pragma: no cover
            raise EnvironmentError("Unable to run tests because temporary "
                                   "dir '%s' exists" % self.path)

    def tearDown (self):
        if os.path.lexists(self.path):
            for dirpath, dirnames, filenames in os.walk(self.path, topdown=False):
                for name in filenames:
                    os.unlink(os.path.join(dirpath, name))

                for name in dirnames:
                    os.rmdir(os.path.join(dirpath, name))

            os.rmdir(self.path)

    def test_get_unrestricted_from_memory (self):
        class Person (Entity):
            pk = Field(Integer, primary_key=True)
            firstname = Field(String)
            surname = Field(String)

        p1 = Person(pk=1, firstname='Homer', surname='Simpson')
        p2 = Person(pk=2, firstname='Bart', surname='Simpson')

        q = Query(Person)

        self.assertEqual(q.get(1), p1)
        self.assertEqual(q.get(2), p2)
        self.assertEqual(q.get(3), None)

        self.assertTrue(p1 in q.all())
        self.assertTrue(p2 in q.all())
        self.assertEqual(len(q.all()), 2)

    def test_get_unrestricted_from_disk (self):
        class Person (Entity):
            pk = Field(Integer, primary_key=True)
            firstname = Field(String)
            surname = Field(String)

        p1 = Person(pk=1, firstname='Homer', surname='Simpson')
        p2 = Person(pk=2, firstname='Bart', surname='Simpson')

        Session.default.store(p1)
        Session.default.store(p2)
        Session.default.expunge()

        q = Query(Person)

        self.assertEqual(q.get(1), p1)
        self.assertEqual(q.get(2), p2)
        self.assertEqual(q.get(3), None)

        self.assertTrue(p1 in q.all())
        self.assertTrue(p2 in q.all())
        self.assertEqual(len(q.all()), 2)

    def test_get_unrestricted_mixed (self):
        class Person (Entity):
            pk = Field(Integer, primary_key=True)
            firstname = Field(String)
            surname = Field(String)

        p1 = Person(pk=1, firstname='Homer', surname='Simpson')

        Session.default.store(p1)
        Session.default.expunge()

        p2 = Person(pk=2, firstname='Bart', surname='Simpson')

        q = Query(Person)

        self.assertEqual(q.get(1), p1)
        self.assertEqual(q.get(2), p2)
        self.assertEqual(q.get(3), None)

        self.assertTrue(p1 in q.all())
        self.assertTrue(p2 in q.all())
        self.assertEqual(len(q.all()), 2)
