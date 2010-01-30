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


class TestQueryFilterBy (TestCase):

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

    def test_filter_by_unrestricted_from_memory (self):
        class Person (Entity):
            pk = Field(Integer, primary_key=True)
            firstname = Field(String)
            surname = Field(String)

        p1 = Person(pk=1, firstname='Homer', surname='Simpson')
        p2 = Person(pk=2, firstname='Bart', surname='Simpson')

        q = Query(Person)

        self.assertEqual(q.filter_by(Person.pk == 1).one(), p1)
        self.assertEqual(q.filter_by(Person.pk == 1).all(), [p1])
        self.assertEqual(q.filter_by(Person.pk == 2).one(), p2)
        self.assertEqual(q.filter_by(Person.pk == 2).all(), [p2])
        self.assertEqual(q.filter_by(Person.pk == 3).one(), None)
        self.assertEqual(q.filter_by(Person.pk == 3).all(), [])

        self.assertEqual(q.filter_by(Person.firstname == 'Homer').one(), p1)
        self.assertEqual(q.filter_by(Person.firstname == 'Bart').one(), p2)
        self.assertEqual(q.filter_by(Person.firstname == 'Marge').one(), None)

        self.assertTrue(p1 in q.filter_by(Person.surname == 'Simpson').all())
        self.assertTrue(p2 in q.filter_by(Person.surname == 'Simpson').all())
        self.assertEqual(len(q.filter_by(Person.surname == 'Simpson').all()), 2)

        self.assertEqual(q.filter_by(Person.firstname == 'Homer',
                                     Person.surname == 'Simpson').one(), p1)
        self.assertEqual(q.filter_by(Person.firstname == 'Marge',
                                     Person.surname == 'Simpson').one(), None)
        self.assertEqual(q.filter_by(Person.firstname == 'Homer',
                                     Person.surname == 'Flanders').one(), None)

    def test_filter_by_unrestricted_compound_from_memory (self):
        class Person (Entity):
            pk = Field(Integer, primary_key=True)
            firstname = Field(String)
            surname = Field(String)

        p1 = Person(pk=1, firstname='Homer', surname='Simpson')
        p2 = Person(pk=2, firstname='Bart', surname='Simpson')

        q = Query(Person)

        self.assertEqual(q.filter_by(Person.firstname == 'Homer',
                                     Person.surname == 'Simpson').one(), p1)
        self.assertEqual(q.filter_by(Person.firstname == 'Marge',
                                     Person.surname == 'Simpson').one(), None)
        self.assertEqual(q.filter_by(Person.firstname == 'Homer',
                                     Person.surname == 'Flanders').one(), None)

        self.assertEqual(q.filter_by((Person.firstname == 'Homer') &
                                     (Person.surname == 'Simpson')).one(), p1)
        self.assertEqual(q.filter_by((Person.firstname == 'Marge') &
                                     (Person.surname == 'Simpson')).one(), None)
        self.assertEqual(q.filter_by((Person.firstname == 'Homer') &
                                     (Person.surname == 'Flanders')).one(), None)
        self.assertEqual(q.filter_by((Person.firstname == 'Homer') |
                                     (Person.surname == 'Flanders')).one(), p1)
        self.assertEqual(q.filter_by((Person.firstname == 'Homer') &
                                     ~(Person.surname == 'Flanders')).one(), p1)
        self.assertEqual(q.filter_by(~(Person.firstname == 'Homer') &
                                     ~(Person.surname == 'Flanders')).one(), p2)

    def test_filter_by_unrestricted_from_disk (self):
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

        self.assertEqual(q.filter_by(Person.pk == 1).one(), p1)
        self.assertEqual(q.filter_by(Person.pk == 1).all(), [p1])
        self.assertEqual(q.filter_by(Person.pk == 2).one(), p2)
        self.assertEqual(q.filter_by(Person.pk == 2).all(), [p2])
        self.assertEqual(q.filter_by(Person.pk == 3).one(), None)
        self.assertEqual(q.filter_by(Person.pk == 3).all(), [])

        self.assertEqual(q.filter_by(Person.firstname == 'Homer').one(), p1)
        self.assertEqual(q.filter_by(Person.firstname == 'Bart').one(), p2)
        self.assertEqual(q.filter_by(Person.firstname == 'Marge').one(), None)

        self.assertTrue(p1 in q.filter_by(Person.surname == 'Simpson').all())
        self.assertTrue(p2 in q.filter_by(Person.surname == 'Simpson').all())
        self.assertEqual(len(q.filter_by(Person.surname == 'Simpson').all()), 2)

        self.assertEqual(q.filter_by(Person.firstname == 'Homer',
                                     Person.surname == 'Simpson').one(), p1)
        self.assertEqual(q.filter_by(Person.firstname == 'Marge',
                                     Person.surname == 'Simpson').one(), None)
        self.assertEqual(q.filter_by(Person.firstname == 'Homer',
                                     Person.surname == 'Flanders').one(), None)

    def test_filter_by_unrestricted_compound_from_disk (self):
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

        self.assertEqual(q.filter_by(Person.firstname == 'Homer',
                                     Person.surname == 'Simpson').one(), p1)
        self.assertEqual(q.filter_by(Person.firstname == 'Marge',
                                     Person.surname == 'Simpson').one(), None)
        self.assertEqual(q.filter_by(Person.firstname == 'Homer',
                                     Person.surname == 'Flanders').one(), None)

        self.assertEqual(q.filter_by((Person.firstname == 'Homer') &
                                     (Person.surname == 'Simpson')).one(), p1)
        self.assertEqual(q.filter_by((Person.firstname == 'Marge') &
                                     (Person.surname == 'Simpson')).one(), None)
        self.assertEqual(q.filter_by((Person.firstname == 'Homer') &
                                     (Person.surname == 'Flanders')).one(), None)
        self.assertEqual(q.filter_by((Person.firstname == 'Homer') |
                                     (Person.surname == 'Flanders')).one(), p1)
        self.assertEqual(q.filter_by((Person.firstname == 'Homer') &
                                     ~(Person.surname == 'Flanders')).one(), p1)
        self.assertEqual(q.filter_by(~(Person.firstname == 'Homer') &
                                     ~(Person.surname == 'Flanders')).one(), p2)

    def test_filter_by_unrestricted_mixed (self):
        class Person (Entity):
            pk = Field(Integer, primary_key=True)
            firstname = Field(String)
            surname = Field(String)

        p1 = Person(pk=1, firstname='Homer', surname='Simpson')

        Session.default.store(p1)
        Session.default.expunge()

        p2 = Person(pk=2, firstname='Bart', surname='Simpson')

        q = Query(Person)

        self.assertEqual(q.filter_by(Person.pk == 1).one(), p1)
        self.assertEqual(q.filter_by(Person.pk == 1).all(), [p1])
        self.assertEqual(q.filter_by(Person.pk == 2).one(), p2)
        self.assertEqual(q.filter_by(Person.pk == 2).all(), [p2])
        self.assertEqual(q.filter_by(Person.pk == 3).one(), None)
        self.assertEqual(q.filter_by(Person.pk == 3).all(), [])

        self.assertEqual(q.filter_by(Person.firstname == 'Homer').one(), p1)
        self.assertEqual(q.filter_by(Person.firstname == 'Bart').one(), p2)
        self.assertEqual(q.filter_by(Person.firstname == 'Marge').one(), None)

        self.assertTrue(p1 in q.filter_by(Person.surname == 'Simpson').all())
        self.assertTrue(p2 in q.filter_by(Person.surname == 'Simpson').all())
        self.assertEqual(len(q.filter_by(Person.surname == 'Simpson').all()), 2)

        self.assertEqual(q.filter_by(Person.firstname == 'Homer',
                                     Person.surname == 'Simpson').one(), p1)
        self.assertEqual(q.filter_by(Person.firstname == 'Marge',
                                     Person.surname == 'Simpson').one(), None)
        self.assertEqual(q.filter_by(Person.firstname == 'Homer',
                                     Person.surname == 'Flanders').one(), None)

    def test_filter_by_unrestricted_compound_mixed (self):
        class Person (Entity):
            pk = Field(Integer, primary_key=True)
            firstname = Field(String)
            surname = Field(String)

        p1 = Person(pk=1, firstname='Homer', surname='Simpson')

        Session.default.store(p1)
        Session.default.expunge()

        p2 = Person(pk=2, firstname='Bart', surname='Simpson')

        q = Query(Person)

        self.assertEqual(q.filter_by(Person.firstname == 'Homer',
                                     Person.surname == 'Simpson').one(), p1)
        self.assertEqual(q.filter_by(Person.firstname == 'Marge',
                                     Person.surname == 'Simpson').one(), None)
        self.assertEqual(q.filter_by(Person.firstname == 'Homer',
                                     Person.surname == 'Flanders').one(), None)

        self.assertEqual(q.filter_by((Person.firstname == 'Homer') &
                                     (Person.surname == 'Simpson')).one(), p1)
        self.assertEqual(q.filter_by((Person.firstname == 'Marge') &
                                     (Person.surname == 'Simpson')).one(), None)
        self.assertEqual(q.filter_by((Person.firstname == 'Homer') &
                                     (Person.surname == 'Flanders')).one(), None)
        self.assertEqual(q.filter_by((Person.firstname == 'Homer') |
                                     (Person.surname == 'Flanders')).one(), p1)
        self.assertEqual(q.filter_by((Person.firstname == 'Homer') &
                                     ~(Person.surname == 'Flanders')).one(), p1)
        self.assertEqual(q.filter_by(~(Person.firstname == 'Homer') &
                                     ~(Person.surname == 'Flanders')).one(), p2)

    def test_filter_by_unrestricted_integer (self):
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

        self.assertTrue('__eq__' in dir(Person.pk))
        self.assertTrue('__ne__' in dir(Person.pk))
        self.assertTrue('__lt__' in dir(Person.pk))
        self.assertTrue('__le__' in dir(Person.pk))
        self.assertTrue('__ge__' in dir(Person.pk))
        self.assertTrue('__gt__' in dir(Person.pk))

        self.assertFalse('__lt__' in dir(Person.firstname))
        self.assertFalse('__le__' in dir(Person.firstname))
        self.assertFalse('__ge__' in dir(Person.firstname))
        self.assertFalse('__gt__' in dir(Person.firstname))

        self.assertEqual(q.filter_by(Person.pk == 1).one(), p1)
        self.assertEqual(q.filter_by(Person.pk == 2).one(), p2)
        self.assertEqual(q.filter_by(Person.pk == 3).one(), None)

        self.assertEqual(q.filter_by(Person.pk < 1).one(), None)
        self.assertEqual(q.filter_by(Person.pk < 2).one(), p1)

        self.assertEqual(q.filter_by(Person.pk <= 0).one(), None)
        self.assertEqual(q.filter_by(Person.pk <= 1).one(), p1)

        self.assertEqual(q.filter_by(Person.pk >= 2).one(), p2)
        self.assertEqual(q.filter_by(Person.pk >= 3).one(), None)

        self.assertEqual(q.filter_by(Person.pk > 1).one(), p2)
        self.assertEqual(q.filter_by(Person.pk > 2).one(), None)

        self.assertEqual(q.filter_by((Person.pk >= 1) & (Person.pk <= 1)).one(), p1)
        self.assertEqual(q.filter_by((Person.pk >= 1) & ~(Person.pk > 1)).one(), p1)

    def test_filter_by_unrestricted_string (self):
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

        self.assertTrue('__eq__' in dir(Person.firstname))
        self.assertTrue('__ne__' in dir(Person.firstname))
        self.assertTrue('startswith' in dir(Person.firstname))
        self.assertTrue('contains' in dir(Person.firstname))
        self.assertTrue('endswith' in dir(Person.firstname))

        self.assertFalse('startswith' in dir(Person.pk))
        self.assertFalse('contains' in dir(Person.pk))
        self.assertFalse('endswith' in dir(Person.pk))

        self.assertEqual(q.filter_by(Person.firstname == 'Homer').one(), p1)
        self.assertEqual(q.filter_by(Person.firstname == 'Bart').one(), p2)
        self.assertEqual(q.filter_by(Person.firstname == 'Marge').one(), None)

        self.assertEqual(q.filter_by(Person.firstname.startswith('H')).one(), p1)
        self.assertEqual(q.filter_by(Person.firstname.startswith('Bar')).one(), p2)
        self.assertEqual(q.filter_by(Person.firstname.startswith('M')).one(), None)

        self.assertEqual(q.filter_by(Person.firstname.contains('m')).one(), p1)
        self.assertEqual(q.filter_by(Person.firstname.contains('ar')).one(), p2)
        self.assertEqual(q.filter_by(Person.firstname.contains('g')).one(), None)

        self.assertEqual(q.filter_by(Person.firstname.endswith('r')).one(), p1)
        self.assertEqual(q.filter_by(Person.firstname.endswith('rt')).one(), p2)
        self.assertEqual(q.filter_by(Person.firstname.endswith('e')).one(), None)
