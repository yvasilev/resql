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


class TestEntityOneToMany (TestCase):

    def setUp (self):
        Session.default.expunge()

    def test_onetomany_definition_by_class (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        class Home (Entity):
            address = Field(String)
            person = Field(OneToMany, entity=Person)

    def test_onetomany_definition_by_name (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        class Home (Entity):
            address = Field(String)
            person = Field(OneToMany, entity='Person')

    def test_onetomany_instantiation_by_class (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        p = Person(firstname='Homer', surname='Simpson')

        class Home (Entity):
            address = Field(String)
            person = Field(OneToMany, entity=Person)

        h = Home(address='742 Evergreen', person=[p])

    def test_onetomany_instantiation_by_name (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        p = Person(firstname='Homer', surname='Simpson')

        class Home (Entity):
            address = Field(String)
            person = Field(OneToMany, entity='Person')

        h = Home(address='742 Evergreen', person=[p])

    def test_onetomany_attribute_access_by_class (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        p = Person(firstname='Homer', surname='Simpson')

        class Home (Entity):
            address = Field(String)
            person = Field(OneToMany, entity=Person)

        h = Home(address='742 Evergreen', person=[p])

        self.assertEqual(h.person[0], p)
        self.assertEqual(h.person[0].firstname, 'Homer')
        self.assertEqual(h.person[0].surname, 'Simpson')

    def test_onetomany_attribute_access_by_name (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        p = Person(firstname='Homer', surname='Simpson')

        class Home (Entity):
            address = Field(String)
            person = Field(OneToMany, entity='Person')

        h = Home(address='742 Evergreen', person=[p])

        self.assertEqual(h.person[0], p)
        self.assertEqual(h.person[0].firstname, 'Homer')
        self.assertEqual(h.person[0].surname, 'Simpson')

    def test_onetomany_empty_by_class (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        p = Person(firstname='Homer', surname='Simpson')

        class Home (Entity):
            address = Field(String)
            person = Field(OneToMany, entity=Person)

        h = Home(address='742 Evergreen')

        self.assertFalse(h.person)
        self.assertEqual(h.person, [])
        self.assertTrue(h.person == [])
        self.assertFalse(h.person != [])

    def test_onetomany_empty_by_name (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        p = Person(firstname='Homer', surname='Simpson')

        class Home (Entity):
            address = Field(String)
            person = Field(OneToMany, entity='Person')

        h = Home(address='742 Evergreen')

        self.assertFalse(h.person)
        self.assertEqual(h.person, [])
        self.assertTrue(h.person == [])
        self.assertFalse(h.person != [])
