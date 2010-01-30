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

from tesql.orm import *
from tesql.types import *


class TestEntityManyToOne (TestCase):

    def setUp (self):
        Session.default.expunge()

    def test_manytoone_definition_by_class (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        class Account (Entity):
            homedir = Field(String)
            person = Field(ManyToOne, entity=Person)

    def test_manytoone_definition_by_name (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        class Account (Entity):
            homedir = Field(String)
            person = Field(ManyToOne, entity='Person')

    def test_manytoone_instantiation_by_class (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        p = Person(firstname='Homer', surname='Simpson')

        class Account (Entity):
            homedir = Field(String)
            person = Field(ManyToOne, entity=Person)

        a = Account(homedir='/home/hsimpson', person=p)

    def test_manytoone_instantiation_by_name (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        p = Person(firstname='Homer', surname='Simpson')

        class Account (Entity):
            homedir = Field(String)
            person = Field(ManyToOne, entity='Person')

        a = Account(homedir='/home/hsimpson', person=p)

    def test_manytoone_attribute_access_by_class (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        p = Person(firstname='Homer', surname='Simpson')

        class Account (Entity):
            homedir = Field(String)
            person = Field(ManyToOne, entity=Person)

        a = Account(homedir='/home/hsimpson', person=p)

        self.assertEqual(a.person, p)
        self.assertEqual(a.person.firstname, 'Homer')
        self.assertEqual(a.person.surname, 'Simpson')

    def test_manytoone_attribute_access_by_name (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        p = Person(firstname='Homer', surname='Simpson')

        class Account (Entity):
            homedir = Field(String)
            person = Field(ManyToOne, entity='Person')

        a = Account(homedir='/home/hsimpson', person=p)

        self.assertEqual(a.person, p)
        self.assertEqual(a.person.firstname, 'Homer')
        self.assertEqual(a.person.surname, 'Simpson')

    def test_manytoone_required_by_class (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        p = Person(firstname='Homer', surname='Simpson')

        class Account1 (Entity):
            homedir = Field(String)
            person = Field(ManyToOne, entity=Person)

        a = Account1(homedir='/home/hsimpson')

        self.assertFalse(a.person)
        self.assertEqual(a.person, None)
        self.assertTrue(a.person == None)
        self.assertFalse(a.person != None)

        class Account2 (Entity):
            homedir = Field(String)
            person = Field(ManyToOne, entity=Person, required=True)

        self.assertRaises(ValueError, Account2, homedir='/home/hsimpson')

    def test_manytoone_required_by_name (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        p = Person(firstname='Homer', surname='Simpson')

        class Account1 (Entity):
            homedir = Field(String)
            person = Field(ManyToOne, entity='Person')

        a = Account1(homedir='/home/hsimpson')

        self.assertFalse(a.person)
        self.assertEqual(a.person, None)
        self.assertTrue(a.person == None)
        self.assertFalse(a.person != None)

        class Account2 (Entity):
            homedir = Field(String)
            person = Field(ManyToOne, entity='Person', required=True)

        self.assertRaises(ValueError, Account2, homedir='/home/hsimpson')

    def test_manytoone_inverse_relation (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        p = Person(firstname='Homer', surname='Simpson')

        self.assertFalse(hasattr(Person, 'accounts'))
        self.assertFalse(hasattr(p, 'accounts'))

        class Account (Entity):
            homedir = Field(String)
            person = Field(ManyToOne, entity='Person', primary_key=True)

        p = Person(firstname='Homer', surname='Simpson')

        self.assertTrue(hasattr(Person, 'accounts'))
        self.assertTrue(hasattr(p, 'accounts'))

        self.assertEqual(p.accounts, [])

        a = Account(homedir='/home/hsimpson', person=p)

        self.assertEqual(p.accounts, [a])
