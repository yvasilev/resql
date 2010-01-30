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

class TestEntityInit (TestCase):

    def setUp (self):
        Session.default.expunge()

    def test_field_typeerror_by_class (self):
        try:
            class Person (Entity):
                firstname = Field(str)
        except Exception, e:
            self.assertTrue(isinstance(e, TypeError))

    def test_field_typeerror_by_object (self):
        try:
            class Person (Entity):
                firstname = Field(str())
        except Exception, e:
            self.assertTrue(isinstance(e, TypeError))

    def test_field_init_assignment_by_class (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        self.assertEqual(Person.firstname.name, 'firstname')
        self.assertEqual(Person.surname.name, 'surname')

        p1 = Person(firstname='Homer')
        p2 = Person(firstname='Bart')

        self.assertEqual(p1.pk, 0)
        self.assertEqual(p1.firstname, 'Homer')
        self.assertEqual(p1.surname, '')
        self.assertEqual(p2.pk, 1)
        self.assertEqual(p2.firstname, 'Bart')
        self.assertEqual(p2.surname, '')

    def test_field_init_assignment_by_object (self):
        class Person (Entity):
            firstname = Field(String())
            surname = Field(String())

        self.assertEqual(Person.firstname.name, 'firstname')
        self.assertEqual(Person.surname.name, 'surname')

        p1 = Person(firstname='Homer')
        p2 = Person(firstname='Bart')

        self.assertEqual(p1.pk, 0)
        self.assertEqual(p1.firstname, 'Homer')
        self.assertEqual(p1.surname, '')
        self.assertEqual(p2.pk, 1)
        self.assertEqual(p2.firstname, 'Bart')
        self.assertEqual(p2.surname, '')

    def test_field_default_by_class (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String, default='Simpson')

        self.assertEqual(Person.firstname.name, 'firstname')
        self.assertEqual(Person.surname.name, 'surname')

        p1 = Person(firstname='Homer')
        p2 = Person(firstname='Bart')

        self.assertEqual(p1.pk, 0)
        self.assertEqual(p1.firstname, 'Homer')
        self.assertEqual(p1.surname, 'Simpson')
        self.assertEqual(p2.pk, 1)
        self.assertEqual(p2.firstname, 'Bart')
        self.assertEqual(p2.surname, 'Simpson')

    def test_field_default_by_object (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String(), default='Simpson')

        self.assertEqual(Person.firstname.name, 'firstname')
        self.assertEqual(Person.surname.name, 'surname')

        p1 = Person(firstname='Homer')
        p2 = Person(firstname='Bart')

        self.assertEqual(p1.pk, 0)
        self.assertEqual(p1.firstname, 'Homer')
        self.assertEqual(p1.surname, 'Simpson')
        self.assertEqual(p2.pk, 1)
        self.assertEqual(p2.firstname, 'Bart')
        self.assertEqual(p2.surname, 'Simpson')
