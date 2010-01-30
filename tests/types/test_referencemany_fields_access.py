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
from tesql.types.references import ReferenceMany


class TestReferenceManyFieldsAccess (TestCase):

    def setUp (self):
        Session.default.expunge()

    def test_type_by_pk (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        p = Person(firstname='Homer', surname='Simpson')

        r = ReferenceMany()
        r.bind_to_entity(Person)

        r.set_data([p.entity_pk_value])

        self.assertTrue(isinstance(r.get_data(), ReferenceMany))
        self.assertTrue(isinstance(r[0], Entity))

    def test_type_by_instance (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        p = Person(firstname='Homer', surname='Simpson')

        r = ReferenceMany()
        r.bind_to_entity(Person)

        r.set_data([p])

        self.assertTrue(isinstance(r.get_data(), ReferenceMany))
        self.assertTrue(isinstance(r[0], Entity))

    def test_fields_value_by_pk (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')

        r = ReferenceMany()
        r.bind_to_entity(Person)

        self.assertFalse(p1 in r)
        self.assertFalse(p2 in r)

        r.set_data([p1.entity_pk_value])

        self.assertTrue(p1 in r)
        self.assertFalse(p2 in r)

        self.assertEqual(r[0].firstname, 'Homer')
        self.assertEqual(r[0].surname, 'Simpson')

        r.set_data([p2.entity_pk_value])

        self.assertFalse(p1 in r)
        self.assertTrue(p2 in r)

        self.assertEqual(r[0].firstname, 'Bart')
        self.assertEqual(r[0].surname, 'Simpson')

        r.append(p1.entity_pk_value)

        self.assertTrue(p1 in r)
        self.assertTrue(p2 in r)

        self.assertEqual(r[0].firstname, 'Bart')
        self.assertEqual(r[0].surname, 'Simpson')
        self.assertEqual(r[1].firstname, 'Homer')
        self.assertEqual(r[1].surname, 'Simpson')

    def test_fields_value_by_instance (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')

        r = ReferenceMany()
        r.bind_to_entity(Person)

        self.assertFalse(p1 in r)
        self.assertFalse(p2 in r)

        r.set_data([p1])

        self.assertTrue(p1 in r)
        self.assertFalse(p2 in r)

        self.assertEqual(r[0].firstname, 'Homer')
        self.assertEqual(r[0].surname, 'Simpson')

        r.set_data([p2])

        self.assertFalse(p1 in r)
        self.assertTrue(p2 in r)

        self.assertEqual(r[0].firstname, 'Bart')
        self.assertEqual(r[0].surname, 'Simpson')

        r.append(p1)

        self.assertTrue(p1 in r)
        self.assertTrue(p2 in r)

        self.assertEqual(r[0].firstname, 'Bart')
        self.assertEqual(r[0].surname, 'Simpson')
        self.assertEqual(r[1].firstname, 'Homer')
        self.assertEqual(r[1].surname, 'Simpson')
