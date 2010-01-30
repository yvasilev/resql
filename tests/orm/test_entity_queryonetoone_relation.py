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


class TestEntityQueryOneToOne (TestCase):

    def setUp (self):
        Session.default.expunge()

    def test_queryone_definition_by_class (self):
        class Account (Entity):
            homedir = Field(String)
            person = Field(OneToOne, entity='Person')

        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)
            account = Field(QueryOneToOne, entity=Account, inverse='person',
                            virtual=True)

    def test_queryone_definition_by_name (self):
        class Account (Entity):
            homedir = Field(String)
            person = Field(OneToOne, entity='Person')

        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)
            account = Field(QueryOneToOne, entity='Account', inverse='person',
                            virtual=True)

    def test_onetoone_instantiation_by_class (self):
        class Account (Entity):
            homedir = Field(String)
            person = Field(OneToOne, entity='Person')

        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)
            account = Field(QueryOneToOne, entity=Account, inverse='person',
                            virtual=True)

        p = Person(firstname='Homer', surname='Simpson')

        a = Account(homedir='/home/hsimpson', person=p)

    def test_onetoone_instantiation_by_name (self):
        class Account (Entity):
            homedir = Field(String)
            person = Field(OneToOne, entity='Person')

        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)
            account = Field(QueryOneToOne, entity='Account', inverse='person',
                            virtual=True)

        p = Person(firstname='Homer', surname='Simpson')

        a = Account(homedir='/home/hsimpson', person=p)

    def test_onetoone_attribute_access_by_class (self):
        class Account (Entity):
            homedir = Field(String)
            person = Field(OneToOne, entity='Person')

        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)
            account = Field(QueryOneToOne, entity=Account, inverse='person',
                            virtual=True)

        p = Person(firstname='Homer', surname='Simpson')

        a = Account(homedir='/home/hsimpson', person=p)

        self.assertEqual(a.person, p)
        self.assertEqual(p.account, a)
        self.assertEqual(p.account.homedir, '/home/hsimpson')

    def test_onetoone_attribute_access_by_name (self):
        class Account (Entity):
            homedir = Field(String)
            person = Field(OneToOne, entity='Person')

        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)
            account = Field(QueryOneToOne, entity='Account', inverse='person',
                            virtual=True)

        p = Person(firstname='Homer', surname='Simpson')

        a = Account(homedir='/home/hsimpson', person=p)

        self.assertEqual(a.person, p)
        self.assertEqual(p.account, a)
        self.assertEqual(p.account.homedir, '/home/hsimpson')

    def test_queryone_as_inverse_relation (self):
        class Account (Entity):
            homedir = Field(String)
            person = Field(OneToOne, entity='Person')

        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)
            account = Field(QueryOneToOne, entity='Account', inverse='person',
                            virtual=True)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')

        a = Account(homedir='/home/hsimpson', person=p1)

        self.assertEqual(a.person, p1)
        self.assertEqual(p1.account, a)
        self.assertEqual(p2.account, None)

        p2.account = a

        self.assertEqual(a.person, p2)
        self.assertEqual(p1.account, None)
        self.assertEqual(p2.account, a)
