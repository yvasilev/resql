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

class TestQuerySortBy (TestCase):

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

    def test_sorted_by_unrestricted_from_memory (self):
        class Person (Entity):
            pk = Field(Integer, primary_key=True)
            firstname = Field(String)
            surname = Field(String)

        p1 = Person(pk=1, firstname='Homer', surname='Simpson')
        p2 = Person(pk=2, firstname='Bart', surname='Simpson')
        p3 = Person(pk=3, firstname='Carl', surname='Carlson')

        q = Query(Person)

        self.assertEqual(q.sort_by(Person.pk.ascending).all(), [p1, p2, p3])
        self.assertEqual(q.sort_by(Person.pk.descending).all(), [p3, p2, p1])

        self.assertEqual(q.sort_by(Person.firstname.ascending).all(), [p2, p3, p1])
        self.assertEqual(q.sort_by(Person.firstname.descending).all(), [p1, p3, p2])

        self.assertEqual(q.sort_by(Person.surname.ascending,
                                   Person.firstname.ascending).all(), [p3, p2, p1])
        self.assertEqual(q.sort_by(Person.surname.ascending,
                                   Person.firstname.descending).all(), [p3, p1, p2])
        self.assertEqual(q.sort_by(Person.surname.descending,
                                   Person.firstname.ascending).all(), [p2, p1, p3])
        self.assertEqual(q.sort_by(Person.surname.descending,
                                   Person.firstname.descending).all(), [p1, p2, p3])

    def test_sorted_by_unrestricted_from_disk (self):
        class Person (Entity):
            pk = Field(Integer, primary_key=True)
            firstname = Field(String)
            surname = Field(String)

        p1 = Person(pk=1, firstname='Homer', surname='Simpson')
        p2 = Person(pk=2, firstname='Bart', surname='Simpson')
        p3 = Person(pk=3, firstname='Carl', surname='Carlson')

        Session.default.commit()
        Session.default.expunge()

        q = Query(Person)

        self.assertEqual(q.sort_by(Person.pk.ascending).all(), [p1, p2, p3])
        self.assertEqual(q.sort_by(Person.pk.descending).all(), [p3, p2, p1])

        self.assertEqual(q.sort_by(Person.firstname.ascending).all(), [p2, p3, p1])
        self.assertEqual(q.sort_by(Person.firstname.descending).all(), [p1, p3, p2])

        self.assertEqual(q.sort_by(Person.surname.ascending,
                                   Person.firstname.ascending).all(), [p3, p2, p1])
        self.assertEqual(q.sort_by(Person.surname.ascending,
                                   Person.firstname.descending).all(), [p3, p1, p2])
        self.assertEqual(q.sort_by(Person.surname.descending,
                                   Person.firstname.ascending).all(), [p2, p1, p3])
        self.assertEqual(q.sort_by(Person.surname.descending,
                                   Person.firstname.descending).all(), [p1, p2, p3])

    def test_sorted_by_unrestricted_mixed (self):
        class Person (Entity):
            pk = Field(Integer, primary_key=True)
            firstname = Field(String)
            surname = Field(String)

        p1 = Person(pk=1, firstname='Homer', surname='Simpson')

        Session.default.commit()
        Session.default.expunge()

        p2 = Person(pk=2, firstname='Bart', surname='Simpson')
        p3 = Person(pk=3, firstname='Carl', surname='Carlson')

        q = Query(Person)

        self.assertEqual(q.sort_by(Person.pk.ascending).all(), [p1, p2, p3])
        self.assertEqual(q.sort_by(Person.pk.descending).all(), [p3, p2, p1])

        self.assertEqual(q.sort_by(Person.firstname.ascending).all(), [p2, p3, p1])
        self.assertEqual(q.sort_by(Person.firstname.descending).all(), [p1, p3, p2])

        self.assertEqual(q.sort_by(Person.surname.ascending,
                                   Person.firstname.ascending).all(), [p3, p2, p1])
        self.assertEqual(q.sort_by(Person.surname.ascending,
                                   Person.firstname.descending).all(), [p3, p1, p2])
        self.assertEqual(q.sort_by(Person.surname.descending,
                                   Person.firstname.ascending).all(), [p2, p1, p3])
        self.assertEqual(q.sort_by(Person.surname.descending,
                                   Person.firstname.descending).all(), [p1, p2, p3])
