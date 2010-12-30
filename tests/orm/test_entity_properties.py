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


class TestEntityProperties (TestCase):

    def setUp (self):
        Session.default.expunge()

    def test_entity_meta_name_and_pk (self):
        class Person (Entity):
            handle = Field(String, primary_key=True)
            firstname = Field(String)
            surname = Field(String)

        p = Person(handle='hsimpson', firstname='Homer', surname='Simpson')

        self.assertEqual(p.meta.name, 'Person')
        self.assertEqual(p.meta.pk.name, 'handle')
        self.assertEqual(p.pk, 'hsimpson')

        class Account (Entity):
            handle = Field(String, primary_key=True)
            homedir = Field(String)

        a = Account(handle='bsimpson', homedir='/home/hsimpson')

        self.assertEqual(p.meta.name, 'Person')
        self.assertEqual(p.meta.pk.name, 'handle')
        self.assertEqual(p.pk, 'hsimpson')

        self.assertEqual(a.meta.name, 'Account')
        self.assertEqual(a.meta.pk.name, 'handle')
        self.assertEqual(a.pk, 'bsimpson')

    def test_entity_as_dictionary (self):
        class Person (Entity):
            handle = Field(String, primary_key=True)
            firstname = Field(String)
            surname = Field(String)

        p1 = Person(handle='hsimpson', firstname='Homer', surname='Simpson')
        p2 = Person(handle='bsimpson', firstname='Bart', surname='Simpson')

        self.assertEqual(p1.entity_as_dictionary.name, 'Person')
        self.assertEqual(p1.entity_as_dictionary, {'handle': 'hsimpson',
                         'firstname': 'Homer', 'surname': 'Simpson'})

        self.assertEqual(p2.entity_as_dictionary.name, 'Person')
        self.assertEqual(p2.entity_as_dictionary, {'handle': 'bsimpson',
                         'firstname': 'Bart', 'surname': 'Simpson'})

        class Account (Entity):
            handle = Field(String, primary_key=True)
            homedir = Field(String)

        a = Account(handle='hsimpson', homedir='/home/hsimpson')

        self.assertEqual(p1.entity_as_dictionary.name, 'Person')
        self.assertEqual(p1.entity_as_dictionary, {'handle': 'hsimpson',
                         'firstname': 'Homer', 'surname': 'Simpson'})

        self.assertEqual(p2.entity_as_dictionary.name, 'Person')
        self.assertEqual(p2.entity_as_dictionary, {'handle': 'bsimpson',
                         'firstname': 'Bart', 'surname': 'Simpson'})

        self.assertEqual(a.entity_as_dictionary.name, 'Account')
        self.assertEqual(a.entity_as_dictionary, {'handle': 'hsimpson',
                         'homedir': '/home/hsimpson'})

