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


class TestEntityQueryManyToOne (TestCase):

    def setUp (self):
        Entity.entities = {}
        Session.default.expunge()

    def test_querymany_definition_by_class (self):
        class Account (Entity):
            homedir = Field(String)
            person = Field(ManyToOne, entity='Person')

        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)
            accounts = Field(QueryManyToOne, entity=Account, inverse='person',
                             virtual=True)

    def test_querymany_definition_by_name (self):
        class Account (Entity):
            homedir = Field(String)
            person = Field(ManyToOne, entity='Person')

        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)
            accounts = Field(QueryManyToOne, entity='Account', inverse='person',
                             virtual=True)

    def test_querymany_instantiation_by_class (self):
        class Account (Entity):
            homedir = Field(String)
            person = Field(ManyToOne, entity='Person')

        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)
            accounts = Field(QueryManyToOne, entity=Account, inverse='person',
                             virtual=True)

        p = Person(firstname='Homer', surname='Simpson')
        a = Account(homedir='/home/hsimpson', person=p)

    def test_manytoone_instantiation_by_name (self):
        class Account (Entity):
            homedir = Field(String)
            person = Field(ManyToOne, entity='Person')

        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)
            accounts = Field(QueryManyToOne, entity='Account', inverse='person',
                             virtual=True)

        p = Person(firstname='Homer', surname='Simpson')
        a = Account(homedir='/home/hsimpson', person=p)

    def test_querymany_attribute_access_by_class (self):
        class Account (Entity):
            homedir = Field(String)
            person = Field(ManyToOne, entity='Person')

        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)
            accounts = Field(QueryManyToOne, entity=Account, inverse='person',
                             virtual=True)

        p = Person(firstname='Homer', surname='Simpson')
        a = Account(homedir='/home/hsimpson', person=p)

        self.assertEqual(a.person, p)
        self.assertEqual(p.accounts, [a])
        self.assertEqual(p.accounts[0].homedir, '/home/hsimpson')

    def test_querymany_attribute_access_by_name (self):
        class Account (Entity):
            homedir = Field(String)
            person = Field(ManyToOne, entity='Person')

        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)
            accounts = Field(QueryManyToOne, entity='Account', inverse='person',
                             virtual=True)

        p = Person(firstname='Homer', surname='Simpson')
        a = Account(homedir='/home/hsimpson', person=p)

        self.assertEqual(a.person, p)
        self.assertEqual(p.accounts, [a])
        self.assertEqual(p.accounts[0].homedir, '/home/hsimpson')

    def test_querymany_as_inverse_relation (self):
        class Account (Entity):
            homedir = Field(String)
            person = Field(ManyToOne, entity='Person')

        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)
            accounts = Field(QueryManyToOne, entity=Account, inverse='person',
                             virtual=True)

        p = Person(firstname='Homer', surname='Simpson')
        a1 = Account(homedir='/home/hsimpson', person=p)
        a2 = Account(homedir='/home/homer')

        self.assertEqual(a1.person, p)
        self.assertEqual(a2.person, None)
        self.assertEqual(p.accounts, [a1])

        p.accounts.append(a2)

        self.assertEqual(a1.person, p)
        self.assertEqual(a2.person, p)
        self.assertEqual(p.accounts, [a1, a2])
        self.assertEqual(p.accounts, [a2, a1])

        p.accounts[0] = None

        self.assertEqual(a1.person, None)
        self.assertEqual(a2.person, p)
        self.assertEqual(p.accounts, [a2])

        p.accounts = [a1]

        self.assertEqual(a1.person, p)
        self.assertEqual(a2.person, None)
        self.assertEqual(p.accounts, [a1])

        p.accounts = []

        self.assertEqual(a1.person, None)
        self.assertEqual(a2.person, None)
        self.assertEqual(p.accounts, [])
