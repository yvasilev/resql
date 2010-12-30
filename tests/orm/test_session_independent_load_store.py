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

from tesql.disk.strategies import Independent


class TestSessionIndependentLoadStore (TestCase):

    def setUp (self):
        Entity.entities = {}
        self.path = '/tmp/test.tesqldb'
        Session(strategy=Independent).be_default()
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
        Session().be_default()

    def test_session_cache_stack (self):
        class Person (Entity):
            pk = Field(Integer, primary_key=True)
            firstname = Field(String)
            surname = Field(String)

        p1 = Person(pk=1, firstname='Homer', surname='Simpson')
        p2 = Person(pk=2, firstname='Bart', surname='Simpson')

        self.assertTrue(Session.default._cache.contains(p1))
        self.assertTrue(Session.default._stack.contains(p1))
        self.assertTrue(Session.default._cache.contains(p2))
        self.assertTrue(Session.default._stack.contains(p2))

        self.assertTrue(('Person', 1) in Session.default._cache.keys())
        self.assertTrue(('Person', 2) in Session.default._cache.keys())
        self.assertEqual(len(Session.default._cache.keys()), 2)

        self.assertTrue(('Person', 1) in Session.default._stack.peek().keys())
        self.assertTrue(('Person', 2) in Session.default._stack.peek().keys())
        self.assertEqual(len(Session.default._stack.peek().keys()), 2)

        Session.default.commit()

        self.assertTrue(('Person', 1) in Session.default._cache.keys())
        self.assertTrue(('Person', 2) in Session.default._cache.keys())
        self.assertEqual(len(Session.default._cache.keys()), 2)

        self.assertEqual(Session.default._stack.peek().keys(), [])

        Session.default.expunge()
        self.assertEqual(Session.default._cache.keys(), [])
        self.assertEqual(Session.default._stack.peek().keys(), [])

    def test_session_store (self):
        class Person (Entity):
            pk = Field(Integer, primary_key=True)
            firstname = Field(String)
            surname = Field(String)

        p1 = Person(pk=1, firstname='Homer', surname='Simpson')
        p2 = Person(pk=2, firstname='Bart', surname='Simpson')

        self.assertTrue(Session.default._cache.contains(p1))
        self.assertTrue(Session.default._stack.contains(p1))
        self.assertTrue(Session.default._cache.contains(p2))
        self.assertTrue(Session.default._stack.contains(p2))

        self.assertFalse(os.path.isfile(os.path.join(self.path, 'Person', '1.conf')))
        self.assertFalse(os.path.isfile(os.path.join(self.path, 'Person', '2.conf')))

        Session.default.store(p1)
        Session.default.store(p2)

        self.assertTrue(Session.default._cache.contains(p1))
        self.assertFalse(Session.default._stack.contains(p1))
        self.assertTrue(Session.default._cache.contains(p2))
        self.assertFalse(Session.default._stack.contains(p2))

        self.assertTrue(os.path.isfile(os.path.join(self.path, 'Person', '1.conf')))
        self.assertTrue(os.path.isfile(os.path.join(self.path, 'Person', '2.conf')))

        self.assertEqual(open(os.path.join(self.path, 'Person', '1.conf'), 'rU').read(),
                         '\n[Person]\n\npk: 1\nfirstname: Homer\nsurname: Simpson\n')
        self.assertEqual(open(os.path.join(self.path, 'Person', '2.conf'), 'rU').read(),
                         '\n[Person]\n\npk: 2\nfirstname: Bart\nsurname: Simpson\n')

    def test_session_load (self):
        class Person (Entity):
            pk = Field(Integer, primary_key=True)
            firstname = Field(String)
            surname = Field(String)

        self.assertEqual(list(Session.default.list_primary_keys(Person)), [])

        p1 = Person(pk=1, firstname='Homer', surname='Simpson')
        p2 = Person(pk=2, firstname='Bart', surname='Simpson')

        Session.default.store(p1)
        Session.default.store(p2)

        self.assertTrue(os.path.isfile(os.path.join(self.path, 'Person', '1.conf')))
        self.assertTrue(os.path.isfile(os.path.join(self.path, 'Person', '2.conf')))

        Session.default.expunge()

        np1 = Session.default.get(Person, 1)
        np2 = Session.default.get(Person, 2)

        self.assertTrue(Session.default._cache.contains(np1))
        self.assertFalse(Session.default._stack.contains(np1))
        self.assertTrue(Session.default._cache.contains(np2))
        self.assertFalse(Session.default._stack.contains(np2))

        self.assertTrue(isinstance(np1, Person))
        self.assertEqual(np1.meta.name, 'Person')
        self.assertEqual(np1.pk, 1)
        self.assertEqual(np1.firstname, 'Homer')
        self.assertEqual(np1.surname, 'Simpson')

        self.assertTrue(isinstance(np2, Person))
        self.assertEqual(np2.meta.name, 'Person')
        self.assertEqual(np2.pk, 2)
        self.assertEqual(np2.firstname, 'Bart')
        self.assertEqual(np2.surname, 'Simpson')

    def test_session_get_from_cache (self):
        class Person (Entity):
            pk = Field(Integer, primary_key=True)
            firstname = Field(String)
            surname = Field(String)

        p1 = Person(pk=1, firstname='Homer', surname='Simpson')
        p2 = Person(pk=2, firstname='Bart', surname='Simpson')

        Session.default.commit()

        self.assertTrue(Session.default._cache.contains(p1))
        self.assertFalse(Session.default._stack.contains(p1))
        self.assertTrue(Session.default._cache.contains(p2))
        self.assertFalse(Session.default._stack.contains(p2))

        np1 = Session.default.get(Person, 1)
        np2 = Session.default.get(Person, 2)

        self.assertTrue(Session.default._cache.contains(np1))
        self.assertFalse(Session.default._stack.contains(np1))
        self.assertTrue(Session.default._cache.contains(np2))
        self.assertFalse(Session.default._stack.contains(np2))

        self.assertTrue(isinstance(np1, Person))
        self.assertEqual(np1.meta.name, 'Person')
        self.assertEqual(np1.pk, 1)
        self.assertEqual(np1.firstname, 'Homer')
        self.assertEqual(np1.surname, 'Simpson')

        self.assertTrue(isinstance(np2, Person))
        self.assertEqual(np2.meta.name, 'Person')
        self.assertEqual(np2.pk, 2)
        self.assertEqual(np2.firstname, 'Bart')
        self.assertEqual(np2.surname, 'Simpson')

    def test_session_get_from_disk (self):
        class Person (Entity):
            pk = Field(Integer, primary_key=True)
            firstname = Field(String)
            surname = Field(String)

        p1 = Person(pk=1, firstname='Homer', surname='Simpson')
        p2 = Person(pk=2, firstname='Bart', surname='Simpson')

        Session.default.commit()
        Session.default.expunge()

        self.assertFalse(Session.default._cache.contains(p1))
        self.assertFalse(Session.default._stack.contains(p1))
        self.assertFalse(Session.default._cache.contains(p2))
        self.assertFalse(Session.default._stack.contains(p2))

        np1 = Session.default.get(Person, 1)
        np2 = Session.default.get(Person, 2)

        self.assertTrue(Session.default._cache.contains(np1))
        self.assertFalse(Session.default._stack.contains(np1))
        self.assertTrue(Session.default._cache.contains(np2))
        self.assertFalse(Session.default._stack.contains(np2))

        self.assertTrue(isinstance(np1, Person))
        self.assertEqual(np1.meta.name, 'Person')
        self.assertEqual(np1.pk, 1)
        self.assertEqual(np1.firstname, 'Homer')
        self.assertEqual(np1.surname, 'Simpson')

        self.assertTrue(isinstance(np2, Person))
        self.assertEqual(np2.meta.name, 'Person')
        self.assertEqual(np2.pk, 2)
        self.assertEqual(np2.firstname, 'Bart')
        self.assertEqual(np2.surname, 'Simpson')
