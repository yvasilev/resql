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

from tesql.orm.decorators import options, location

class TestEntityOptions (TestCase):

    def setUp (self):
        self.path = '/tmp/test.tesqldb'
        Session.default.bind(self.path)
        Session.default.expunge()

    def tearDown (self):
        Session().be_default()

    def test_entity_unspecified_location (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        self.assertEqual(Session.default._strategy.get_location(Person),
                         '/tmp/test.tesqldb/Person')

    def test_entity_relative_location_via_options (self):
        # @options(location='person')   # python >= 2.6
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        Person = options(location='person')(Person) # python < 2.6

        self.assertEqual(Session.default._strategy.get_location(Person),
                         '/tmp/test.tesqldb/person')

    def test_entity_relative_location_via_location (self):
        # @location('person')   # python >= 2.6
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        Person = location('person')(Person) # python < 2.6

        self.assertEqual(Session.default._strategy.get_location(Person),
                         '/tmp/test.tesqldb/person')

    def test_entity_absolute_location_via_options (self):
        # @options(location='/etc/person')   # python >= 2.6
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        Person = options(location='/etc/person')(Person) # python < 2.6

        self.assertEqual(Session.default._strategy.get_location(Person),
                         '/etc/person')

    def test_entity_absolute_location_via_location (self):
        # @location('/etc/person')   # python >= 2.6
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        Person = location('/etc/person')(Person) # python < 2.6

        self.assertEqual(Session.default._strategy.get_location(Person),
                         '/etc/person')

    def test_instance_unspecified_location (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        p = Person(firstname='Homer', surname='Simpson')

        self.assertEqual(Session.default._strategy.get_location(p),
                         '/tmp/test.tesqldb/Person/0.conf')

    def test_instance_relative_location_via_options (self):
        # python >= 2.6
        # @options(location={None: 'person', 1: 'bart.conf'})
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        # python < 2.6
        Person = options(location={None: 'person', 1: 'bart.conf'})(Person)

        p1 = Person(firstname='Homer', surname='Simpson')

        self.assertEqual(Session.default._strategy.get_location(p1),
                         '/tmp/test.tesqldb/person/0.conf')

        p2 = Person(firstname='Bart', surname='Simpson')

        self.assertEqual(Session.default._strategy.get_location(p2),
                         '/tmp/test.tesqldb/bart.conf')

    def test_instance_relative_location_via_location (self):
        # python >= 2.6
        # @location({None: 'person', 1: 'bart.conf'})
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        # python < 2.6
        Person = location({None: 'person', 1: 'bart.conf'})(Person)

        p1 = Person(firstname='Homer', surname='Simpson')

        self.assertEqual(Session.default._strategy.get_location(p1),
                         '/tmp/test.tesqldb/person/0.conf')

        p2 = Person(firstname='Bart', surname='Simpson')

        self.assertEqual(Session.default._strategy.get_location(p2),
                         '/tmp/test.tesqldb/bart.conf')

    def test_instance_absolute_location_via_options (self):
        # python >= 2.6
        # @options(location={None: '/etc/person', 1: '/etc/bart.conf'})
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        # python < 2.6
        Person = options(location={None: '/etc/person', 1: '/etc/bart.conf'})(Person)

        p1 = Person(firstname='Homer', surname='Simpson')

        self.assertEqual(Session.default._strategy.get_location(p1),
                         '/etc/person/0.conf')

        p2 = Person(firstname='Bart', surname='Simpson')

        self.assertEqual(Session.default._strategy.get_location(p2),
                         '/etc/bart.conf')

    def test_instance_absolute_location_via_location (self):
        # python >= 2.6
        # @location({None: '/etc/person', 1: '/etc/bart.conf'})
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        # python < 2.6
        Person = location({None: '/etc/person', 1: '/etc/bart.conf'})(Person)

        p1 = Person(firstname='Homer', surname='Simpson')

        self.assertEqual(Session.default._strategy.get_location(p1),
                         '/etc/person/0.conf')

        p2 = Person(firstname='Bart', surname='Simpson')

        self.assertEqual(Session.default._strategy.get_location(p2),
                         '/etc/bart.conf')

    def test_singleton_unspecified_location (self):
        class Person (Entity):
            pk = Field(Integer, primary_key=True, choices=[0])
            firstname = Field(String)
            surname = Field(String)

        self.assertEqual(Session.default._strategy.get_location(Person),
                         '/tmp/test.tesqldb/Person.conf')

        p = Person(firstname='Homer', surname='Simpson')

        self.assertEqual(Session.default._strategy.get_location(p),
                         '/tmp/test.tesqldb/Person.conf')

    def test_singleton_relative_location_via_options (self):
        # python >= 2.6
        # @options(location='person')
        class Person (Entity):
            pk = Field(Integer, primary_key=True, choices=[0])
            firstname = Field(String)
            surname = Field(String)

        # python < 2.6
        Person = options(location='person')(Person)

        self.assertEqual(Session.default._strategy.get_location(Person),
                         '/tmp/test.tesqldb/person.conf')

        p = Person(firstname='Homer', surname='Simpson')

        self.assertEqual(Session.default._strategy.get_location(p),
                         '/tmp/test.tesqldb/person.conf')

    def test_singleton_relative_location_via_location (self):
        # python >= 2.6
        # @location('person')
        class Person (Entity):
            pk = Field(Integer, primary_key=True, choices=[0])
            firstname = Field(String)
            surname = Field(String)

        # python < 2.6
        Person = location('person')(Person)

        self.assertEqual(Session.default._strategy.get_location(Person),
                         '/tmp/test.tesqldb/person.conf')

        p = Person(firstname='Homer', surname='Simpson')

        self.assertEqual(Session.default._strategy.get_location(p),
                         '/tmp/test.tesqldb/person.conf')

    def test_singleton_absolute_location_via_options (self):
        # python >= 2.6
        # @options(location='/etc/person')
        class Person (Entity):
            pk = Field(Integer, primary_key=True, choices=[0])
            firstname = Field(String)
            surname = Field(String)

        # python < 2.6
        Person = options(location='/etc/person')(Person)

        self.assertEqual(Session.default._strategy.get_location(Person),
                         '/etc/person.conf')

        p = Person(firstname='Homer', surname='Simpson')

        self.assertEqual(Session.default._strategy.get_location(p),
                         '/etc/person.conf')

    def test_singleton_absolute_location_via_location (self):
        # python >= 2.6
        # @location('/etc/person')
        class Person (Entity):
            pk = Field(Integer, primary_key=True, choices=[0])
            firstname = Field(String)
            surname = Field(String)

        # python < 2.6
        Person = location('/etc/person')(Person)

        self.assertEqual(Session.default._strategy.get_location(Person),
                         '/etc/person.conf')

        p = Person(firstname='Homer', surname='Simpson')

        self.assertEqual(Session.default._strategy.get_location(p),
                         '/etc/person.conf')
