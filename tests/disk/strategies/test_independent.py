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

from tesql.disk.strategies import Independent

from tesql.orm import *
from tesql.types import *


class TestIndependent (TestCase):

    def setUp (self):
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

    def test_base_default (self):
        s = Independent()

        self.assertEqual(os.path.dirname(s.base_location), os.getcwd())
        self.assertEqual(os.path.basename(s.base_location), '.tesqldb')

    def test_base_bind (self):
        s = Independent()

        self.assertEqual(os.path.dirname(s.base_location), os.getcwd())
        self.assertEqual(os.path.basename(s.base_location), '.tesqldb')

        s.bind(self.path)

        self.assertEqual(os.path.dirname(s.base_location), '/tmp')
        self.assertEqual(os.path.basename(s.base_location), 'test.tesqldb')

    def test_entity_default_by_class_get_location (self):
        s = Independent()
        s.bind(self.path)

        class Person (Entity):
            pk = Field(Integer, primary_key=True)
            firstname = Field(String)
            surname = Field(String)

        self.assertEqual(s.get_location(Person),
                         os.path.join(self.path, 'Person'))

        self.assertFalse(os.path.isdir(os.path.join(self.path, 'Person')))

    def test_entity_default_by_class_make_location (self):
        s = Independent()
        s.bind(self.path)

        class Person (Entity):
            pk = Field(Integer, primary_key=True)
            firstname = Field(String)
            surname = Field(String)

        self.assertEqual(s.make_location(Person),
                         os.path.join(self.path, 'Person'))

        self.assertTrue(os.path.isdir(os.path.join(self.path, 'Person')))

    def test_entity_default_by_class_pk_get_location (self):
        s = Independent()
        s.bind(self.path)

        class Person (Entity):
            pk = Field(Integer, primary_key=True)
            firstname = Field(String)
            surname = Field(String)

        self.assertEqual(s.get_location(Person, pk=1),
                         os.path.join(self.path, 'Person', '1.conf'))

        self.assertFalse(os.path.isdir(os.path.join(self.path, 'Person')))

    def test_entity_default_by_class_pk_make_location (self):
        s = Independent()
        s.bind(self.path)

        class Person (Entity):
            pk = Field(Integer, primary_key=True)
            firstname = Field(String)
            surname = Field(String)

        self.assertEqual(s.make_location(Person, pk=1),
                         os.path.join(self.path, 'Person', '1.conf'))

        self.assertTrue(os.path.isdir(os.path.join(self.path, 'Person')))

    def test_entity_default_by_object_get_location (self):
        s = Independent()
        s.bind(self.path)

        class Person (Entity):
            pk = Field(Integer, primary_key=True)
            firstname = Field(String)
            surname = Field(String)

        p1 = Person(pk=1, firstname='Homer', surname='Simpson')
        p2 = Person(pk=2, firstname='Bart', surname='Simpson')

        self.assertEqual(s.get_location(p1),
                         os.path.join(self.path, 'Person', '1.conf'))
        self.assertEqual(s.get_location(p2),
                         os.path.join(self.path, 'Person', '2.conf'))

        self.assertFalse(os.path.isdir(os.path.join(self.path, 'Person')))

    def test_entity_default_by_object_make_location (self):
        s = Independent()
        s.bind(self.path)

        class Person (Entity):
            pk = Field(Integer, primary_key=True)
            firstname = Field(String)
            surname = Field(String)

        p1 = Person(pk=1, firstname='Homer', surname='Simpson')
        p2 = Person(pk=2, firstname='Bart', surname='Simpson')

        self.assertEqual(s.make_location(p1),
                         os.path.join(self.path, 'Person', '1.conf'))
        self.assertEqual(s.make_location(p2),
                         os.path.join(self.path, 'Person', '2.conf'))

        self.assertTrue(os.path.isdir(os.path.join(self.path, 'Person')))

    def test_store_entity_default_store_location (self):
        s = Independent()
        s.bind(self.path)

        class Person (Entity):
            pk = Field(Integer, primary_key=True)
            firstname = Field(String)
            surname = Field(String)

        p1 = Person(pk=1, firstname='Homer', surname='Simpson')
        p2 = Person(pk=2, firstname='Bart', surname='Simpson')

        s.store_location(p1)
        s.store_location(p2)

        self.assertTrue(os.path.isfile(os.path.join(self.path, 'Person', '1.conf')))
        self.assertTrue(os.path.isfile(os.path.join(self.path, 'Person', '2.conf')))

        self.assertEqual(open(os.path.join(self.path, 'Person', '1.conf'), 'rU').read(),
                         '\n[Person]\n\npk: 1\nfirstname: Homer\nsurname: Simpson\n')
        self.assertEqual(open(os.path.join(self.path, 'Person', '2.conf'), 'rU').read(),
                         '\n[Person]\n\npk: 2\nfirstname: Bart\nsurname: Simpson\n')

    def test_load_entity_default_store_location (self):
        s = Independent()
        s.bind(self.path)

        class Person (Entity):
            pk = Field(Integer, primary_key=True)
            firstname = Field(String)
            surname = Field(String)

        p1 = Person(pk=1, firstname='Homer', surname='Simpson')
        p2 = Person(pk=2, firstname='Bart', surname='Simpson')

        s.store_location(p1)
        s.store_location(p2)

        self.assertTrue(os.path.isfile(os.path.join(self.path, 'Person', '1.conf')))
        self.assertTrue(os.path.isfile(os.path.join(self.path, 'Person', '2.conf')))

        np1 = s.load_location(Person, 1)
        np2 = s.load_location(Person, 2)

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

    def test_list_entity_default_store_location (self):
        s = Independent()
        s.bind(self.path)

        class Person (Entity):
            pk = Field(Integer, primary_key=True)
            firstname = Field(String)
            surname = Field(String)

        p1 = Person(pk=1, firstname='Homer', surname='Simpson')
        p2 = Person(pk=2, firstname='Bart', surname='Simpson')

        s.store_location(p1)
        s.store_location(p2)

        self.assertTrue(os.path.isfile(os.path.join(self.path, 'Person', '1.conf')))
        self.assertTrue(os.path.isfile(os.path.join(self.path, 'Person', '2.conf')))

        self.assertEqual(s.list_location(p1),
                         os.path.join(self.path, 'Person', '1.conf'))
        self.assertEqual(s.list_location(Person, 1),
                         os.path.join(self.path, 'Person', '1.conf'))
        self.assertEqual(s.list_location(p2),
                         os.path.join(self.path, 'Person', '2.conf'))
        self.assertEqual(s.list_location(Person, 2),
                         os.path.join(self.path, 'Person', '2.conf'))
        self.assertEqual(s.list_location(Person, 3), None)
        self.assertEqual(list(s.list_location(Person)),
                         [os.path.join(self.path, 'Person', '1.conf'),
                          os.path.join(self.path, 'Person', '2.conf')])

    def test_store_entity_with_virtual_fields_default_store_location (self):
        s = Independent()
        s.bind(self.path)

        class Person (Entity):
            pk = Field(Integer, primary_key=True)
            firstname = Field(String)
            surname = Field(String, virtual=True)

        p1 = Person(pk=1, firstname='Homer', surname='Simpson')
        p2 = Person(pk=2, firstname='Bart', surname='Simpson')

        s.store_location(p1)
        s.store_location(p2)

        self.assertTrue(os.path.isfile(os.path.join(self.path, 'Person', '1.conf')))
        self.assertTrue(os.path.isfile(os.path.join(self.path, 'Person', '2.conf')))

        self.assertEqual(open(os.path.join(self.path, 'Person', '1.conf'), 'rU').read(),
                         '\n[Person]\n\npk: 1\nfirstname: Homer\n')
        self.assertEqual(open(os.path.join(self.path, 'Person', '2.conf'), 'rU').read(),
                         '\n[Person]\n\npk: 2\nfirstname: Bart\n')

    def test_store_load_entity_with_virtual_pk_default_store_location (self):
        s = Independent()
        s.bind(self.path)

        class Person (Entity):
            pk = Field(Indexer, primary_key=True, autoincrement=True, virtual=True)
            firstname = Field(String)
            surname = Field(String)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')

        s.store_location(p1)
        s.store_location(p2)

        self.assertTrue(os.path.isfile(os.path.join(self.path, 'Person', '0.conf')))
        self.assertTrue(os.path.isfile(os.path.join(self.path, 'Person', '1.conf')))

        self.assertEqual(open(os.path.join(self.path, 'Person', '0.conf'), 'rU').read(),
                         '\n[Person]\n\nfirstname: Homer\nsurname: Simpson\n')
        self.assertEqual(open(os.path.join(self.path, 'Person', '1.conf'), 'rU').read(),
                         '\n[Person]\n\nfirstname: Bart\nsurname: Simpson\n')

        np1 = s.load_location(Person, 0)
        np2 = s.load_location(Person, 1)

        self.assertTrue(isinstance(np1, Person))
        self.assertEqual(np1.meta.name, 'Person')
        self.assertEqual(np1.pk, 0)
        self.assertEqual(np1.firstname, 'Homer')
        self.assertEqual(np1.surname, 'Simpson')

        self.assertTrue(isinstance(np2, Person))
        self.assertEqual(np2.meta.name, 'Person')
        self.assertEqual(np2.pk, 1)
        self.assertEqual(np2.firstname, 'Bart')
        self.assertEqual(np2.surname, 'Simpson')
