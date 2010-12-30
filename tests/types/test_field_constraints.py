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

import sys

from unittest import TestCase

from tesql.orm import *
from tesql.types import *


class TestFieldConstraints (TestCase):

    def setUp (self):
        Session.default.expunge()

    def test_explicit_primary_key_detection_integer (self):
        class Person (Entity):
            pk = Field(Integer, primary_key=True)
            firstname = Field(String)
            surname = Field(String)

        self.assertTrue(Person.pk.is_primary_key)
        self.assertFalse(Person.firstname.is_primary_key)
        self.assertFalse(Person.surname.is_primary_key)

        self.assertEqual(Person.pk.name, 'pk')
        self.assertEqual(Person.firstname.name, 'firstname')
        self.assertEqual(Person.surname.name, 'surname')

        self.assertEqual(Person.meta.pk.name, 'pk')

        p1 = Person(pk=1, firstname='Homer')
        p2 = Person(pk=2, firstname='Bart')

        self.assertEqual(p1.pk, 1)
        self.assertEqual(p1.meta.pk.name, 'pk')

        self.assertEqual(p2.pk, 2)
        self.assertEqual(p2.meta.pk.name, 'pk')

    def test_explicit_primary_key_with_explicit_not_pks (self):
        class Person (Entity):
            pk = Field(Integer, primary_key=True)
            firstname = Field(String, primary_key=False)
            surname = Field(String, primary_key=False)

        self.assertTrue(Person.pk.is_primary_key)
        self.assertFalse(Person.firstname.is_primary_key)
        self.assertFalse(Person.surname.is_primary_key)

        self.assertEqual(Person.pk.name, 'pk')
        self.assertEqual(Person.firstname.name, 'firstname')
        self.assertEqual(Person.surname.name, 'surname')

        self.assertEqual(Person.meta.pk.name, 'pk')

        p1 = Person(pk=1, firstname='Homer')
        p2 = Person(pk=2, firstname='Bart')

        self.assertEqual(p1.pk, 1)
        self.assertEqual(p1.meta.pk.name, 'pk')

        self.assertEqual(p2.pk, 2)
        self.assertEqual(p2.meta.pk.name, 'pk')

    def test_explicit_primary_key_detection_string (self):
        try:
            class Person (Entity):
                pk = Field(Integer)
                firstname = Field(String, primary_key=True)
                surname = Field(String)
        except Exception, e:
            self.assertTrue(isinstance(e, AttributeError))
        else:
            self.assertTrue(false)

    def test_explicit_primary_key_detection_string_no_pk_field (self):
        class Person (Entity):
            firstname = Field(String, primary_key=True)
            surname = Field(String)

        self.assertTrue(Person.firstname.is_primary_key)
        self.assertFalse(Person.surname.is_primary_key)

        self.assertEqual(Person.firstname.name, 'firstname')
        self.assertEqual(Person.surname.name, 'surname')

        self.assertEqual(Person.meta.pk.name, 'firstname')

        p1 = Person(firstname='Homer')
        p2 = Person(firstname='Bart')

        self.assertEqual(p1.firstname, 'Homer')
        self.assertEqual(p1.meta.pk.name, 'firstname')
        self.assertEqual(p1.pk, 'Homer')

        self.assertEqual(p2.firstname, 'Bart')
        self.assertEqual(p2.meta.pk.name, 'firstname')
        self.assertEqual(p2.pk, 'Bart')

    def test_explicit_primary_key_uniqueness_integer (self):
        class Person (Entity):
            pk = Field(Integer, primary_key=True)
            firstname = Field(String)
            surname = Field(String)

        self.assertTrue(Person.pk.is_primary_key)
        self.assertFalse(Person.firstname.is_primary_key)
        self.assertFalse(Person.surname.is_primary_key)

        p1 = Person(pk=1, firstname='Homer', surname='Simpson')
        p2 = Person(pk=2, firstname='Bart', surname='Simpson')

        self.assertEqual(p1.pk, 1)
        self.assertEqual(p2.pk, 2)

        self.assertRaises(ValueError, Person, pk=2, firstname='Marge',
                                surname='Simpson')

    def test_explicit_primary_key_uniqueness_string (self):
        try:
            class Person (Entity):
                pk = Field(Integer)
                firstname = Field(String, primary_key=True)
                surname = Field(String)
        except Exception, e:
            self.assertTrue(isinstance(e, AttributeError))
        else:
            self.assertTrue(false)

    def test_explicit_double_primary_key_keyerror (self):
        try:
            class Person (Entity):
                pki = Field(Integer, primary_key=True)
                pks = Field(String, primary_key=True)
                firstname = Field(String)
        except Exception, e:
            self.assertTrue(isinstance(e, AttributeError))
        else:
            self.assertTrue(false)

    def test_implicit_primary_key (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        self.assertEqual(Person.meta.pk.name, 'pk')
        self.assertTrue(Person.meta.pk.is_primary_key)
        self.assertTrue(Person.pk.is_primary_key)
        self.assertFalse(Person.firstname.is_primary_key)
        self.assertFalse(Person.surname.is_primary_key)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')

        self.assertEqual(p1.pk, 0)
        self.assertEqual(p2.pk, 1)

        p3 = Person(pk=5, firstname='Carl', surname='Carlson')

        self.assertEqual(p3.pk, 5)

        p4 = Person(firstname='Lenny', surname='Leonard')

        self.assertEqual(p4.pk, 6)

    def test_implicit_primary_key_uniqueness (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        self.assertTrue(Person.pk.is_primary_key)
        self.assertFalse(Person.firstname.is_primary_key)
        self.assertFalse(Person.surname.is_primary_key)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')

        self.assertEqual(p1.pk, 0)
        self.assertEqual(p2.pk, 1)

        p3 = Person(pk=5, firstname='Carl', surname='Carlson')

        self.assertEqual(p3.pk, 5)

        self.assertRaises(ValueError, Person, pk=5, firstname='Lenny',
                          surname='Leonard')

    def test_implicit_primary_key_with_explicit_not_pks (self):
        class Person (Entity):
            firstname = Field(String, primary_key=False)
            surname = Field(String, primary_key=False)

        self.assertTrue(Person.pk.is_primary_key)
        self.assertFalse(Person.firstname.is_primary_key)
        self.assertFalse(Person.surname.is_primary_key)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')

        self.assertEqual(p1.pk, 0)
        self.assertEqual(p2.pk, 1)

        p3 = Person(pk=5, firstname='Carl', surname='Carlson')

        self.assertEqual(p3.pk, 5)

        self.assertRaises(ValueError, Person, pk=5, firstname='Lenny',
                          surname='Leonard')

    def test_primary_key_not_boolean_argument_string (self):
        try:
            class Person (Entity):
                pk = Field(Integer, primary_key='lala')
                firstname = Field(String)
        except Exception, e:
            self.assertTrue(isinstance(e, ValueError))

    def test_primary_key_not_boolean_argument_integer (self):
        try:
            class Person (Entity):
                pk = Field(Integer, primary_key=25)
                firstname = Field(String)
        except Exception, e:
            self.assertTrue(isinstance(e, ValueError))

    def test_unique_field (self):
        class Person (Entity):
            firstname = Field(String, unique=True)
            surname = Field(String)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')

        self.assertRaises(ValueError, Person, firstname='Bart', surname='Simpson')

    def test_unique_not_boolean_argument_string (self):
        try:
            class Person (Entity):
                age = Field(Integer, unique='lala')
                firstname = Field(String)
        except Exception, e:
            self.assertTrue(isinstance(e, ValueError))

    def test_unique_not_boolean_argument_integer (self):
        try:
            class Person (Entity):
                pk = Field(Integer, unique=25)
                firstname = Field(String)
        except Exception, e:
            self.assertTrue(isinstance(e, ValueError))

    def test_required_field (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String, required=True)
            age = Field(Integer, required=True)

        p1 = Person(firstname='Homer', surname='Simpson', age=10)
        p2 = Person(firstname='Bart', surname='Simpson', age=38)

        self.assertRaises(ValueError, Person, firstname='Marge')
        self.assertRaises(ValueError, Person, firstname='Marge', surname=None)
        self.assertRaises(ValueError, Person, firstname='Marge', surname='')

        self.assertRaises(ValueError, Person, firstname='Marge', surname='Simpson')
        self.assertRaises(ValueError, Person, firstname='Marge', surname='Simpson',
                                              age=None)
        self.assertRaises(ValueError, Person, firstname='Marge', surname='Simpson',
                                              age=0)

    def test_required_not_boolean_argument_string (self):
        try:
            class Person (Entity):
                pk = Field(Integer, required='lala')
                firstname = Field(String)
        except Exception, e:
            self.assertTrue(isinstance(e, ValueError))

    def test_required_not_boolean_argument_integer (self):
        try:
            class Person (Entity):
                pk = Field(Integer, required=25)
                firstname = Field(String)
        except Exception, e:
            self.assertTrue(isinstance(e, ValueError))

    def test_readonly_field (self):
        class Person (Entity):
            firstname = Field(String, readonly=True)
            surname = Field(String, readonly=True)
            age = Field(Integer)

        p = Person(firstname='Homer', surname='Simpson', age=38,
                   check_on_create=False)

        self.assertEqual(p.age, 38)

        p.age = 39
        self.assertEqual(p.age, 39)

        setattr(p, 'age', 38)
        self.assertEqual(p.age, 38)

        self.assertRaises(ValueError, setattr, p, 'firstname', 'Bart')

        self.assertRaises(ValueError, Person, firstname='Bart', surname='Simpson',
                          age=10)

    def test_readonly_not_boolean_argument_string (self):
        try:
            class Person (Entity):
                pk = Field(Integer, readonly='lala')
                firstname = Field(String)
        except Exception, e:
            self.assertTrue(isinstance(e, ValueError))

    def test_readonly_not_boolean_argument_integer (self):
        try:
            class Person (Entity):
                pk = Field(Integer, readonly=25)
                firstname = Field(String)
        except Exception, e:
            self.assertTrue(isinstance(e, ValueError))

    def test_choices_field (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String, choices=['Simpson', 'Flanders'])

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')
        p3 = Person(firstname='Ned', surname='Flanders')

        self.assertRaises(ValueError, Person, firstname='Carl', surname='Carlson')

    def test_choices_not_iterable_argument_string (self):
        try:
            class Person (Entity):
                pk = Field(Integer, choices='lala')
                firstname = Field(String)
        except Exception, e:
            self.assertTrue(isinstance(e, ValueError))

    def test_choices_not_iterable_argument_integer (self):
        try:
            class Person (Entity):
                pk = Field(Integer, choices=25)
                firstname = Field(String)
        except Exception, e:
            self.assertTrue(isinstance(e, ValueError))

    def test_choices_not_iterable_argument_boolean (self):
        try:
            class Person (Entity):
                pk = Field(Integer, choices=True)
                firstname = Field(String)
        except Exception, e:
            self.assertTrue(isinstance(e, ValueError))

    def test_choices_singleton (self):
        class Person (Entity):
            pk = Field(Indexer, primary_key=True, choices=(0,))
            firstname = Field(String)
            surname = Field(String)

        p = Person(firstname='Homer', surname='Simpson')

        self.assertTrue(Person.meta.singleton)
        self.assertTrue(p.meta.singleton)

        self.assertRaises(ValueError, Person, firstname='Carl', surname='Carlson')

    def test_choices_not_singleton (self):
        class Person (Entity):
            pk = Field(Indexer, primary_key=True, autoincrement=True, choices=(0, 1))
            firstname = Field(String)
            surname = Field(String)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')

        self.assertFalse(Person.meta.singleton)
        self.assertFalse(p1.meta.singleton)
        self.assertFalse(p2.meta.singleton)

        self.assertRaises(ValueError, Person, firstname='Carl', surname='Carlson')
