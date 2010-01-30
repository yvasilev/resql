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


class TestEntityQueryOneToMany (TestCase):

    def setUp (self):
        Session.default.expunge()

    def test_queryonetomany_definition_by_class (self):
        class Home (Entity):
            address = Field(String)
            people = Field(OneToMany, entity='Person')

        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)
            home = Field(QueryOneToMany, entity=Home, inverse='people',
                            virtual=True)

    def test_queryonetomany_definition_by_name (self):
        class Home (Entity):
            address = Field(String)
            people = Field(OneToMany, entity='Person')

        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)
            home = Field(QueryOneToMany, entity='Home', inverse='people',
                            virtual=True)

    def test_queryonetomany_instantiation_by_class (self):
        class Home (Entity):
            address = Field(String)
            people = Field(OneToMany, entity='Person')

        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)
            home = Field(QueryOneToMany, entity=Home, inverse='people',
                            virtual=True)

        p = Person(firstname='Homer', surname='Simpson')

        h = Home(address='742 Evergreen', people=[p])

    def test_quetyonetomany_instantiation_by_name (self):
        class Home (Entity):
            address = Field(String)
            people = Field(OneToMany, entity='Person')

        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)
            home = Field(QueryOneToMany, entity='Home', inverse='people',
                            virtual=True)

        p = Person(firstname='Homer', surname='Simpson')

        h = Home(address='742 Evergreen', people=[p])

    def test_queryonetomany_attribute_access_by_class (self):
        class Home (Entity):
            address = Field(String)
            people = Field(OneToMany, entity='Person')

        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)
            home = Field(QueryOneToMany, entity=Home, inverse='people',
                            virtual=True)

        p = Person(firstname='Homer', surname='Simpson')

        h = Home(address='742 Evergreen', people=[p])

        self.assertEqual(h.people, [p])
        self.assertEqual(p.home, h)
        self.assertEqual(p.home.address, '742 Evergreen')

    def test_queryonetomany_attribute_access_by_name (self):
        class Home (Entity):
            address = Field(String)
            people = Field(OneToMany, entity='Person')

        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)
            home = Field(QueryOneToMany, entity='Home', inverse='people',
                            virtual=True)

        p = Person(firstname='Homer', surname='Simpson')

        h = Home(address='742 Evergreen', people=[p])

        self.assertEqual(h.people, [p])
        self.assertEqual(p.home, h)
        self.assertEqual(p.home.address, '742 Evergreen')

    def test_queryonetomany_as_inverse_relation (self):
        class Home (Entity):
            address = Field(String)
            people = Field(OneToMany, entity='Person')

        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)
            home = Field(QueryOneToMany, entity=Home, inverse='people',
                            virtual=True)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')

        h = Home(address='742 Evergreen', people=[p1])

        self.assertEqual(h.people, [p1])
        self.assertEqual(p1.home, h)
        self.assertEqual(p2.home, None)

        p2.home = h

        self.assertEqual(h.people, [p1, p2])
        self.assertEqual(p1.home, h)
        self.assertEqual(p2.home, h)

        p1.home = None

        self.assertEqual(h.people, [p2])
        self.assertEqual(p1.home, None)
        self.assertEqual(p2.home, h)
