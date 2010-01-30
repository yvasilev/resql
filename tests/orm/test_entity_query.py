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


class TestEntityQuery (TestCase):

    def setUp (self):
        Session.default.expunge()

    def test_get (self):
        class Person (Entity):
            pk = Field(Integer, primary_key=True)
            firstname = Field(String)
            surname = Field(String)

        p1 = Person(pk=1, firstname='Homer', surname='Simpson')
        p2 = Person(pk=2, firstname='Bart', surname='Simpson')

        self.assertEqual(Person.get(1), p1)
        self.assertEqual(Person.get(2), p2)
        self.assertEqual(Person.get(3), None)

    def test_get_by (self):
        class Person (Entity):
            pk = Field(Integer, primary_key=True)
            firstname = Field(String)
            surname = Field(String)

        p1 = Person(pk=1, firstname='Homer', surname='Simpson')
        p2 = Person(pk=2, firstname='Bart', surname='Simpson')

        self.assertEqual(Person.get_by(Person.pk == 1), p1)
        self.assertEqual(Person.get_by(Person.pk == 2), p2)
        self.assertEqual(Person.get_by(Person.pk == 3), None)

        self.assertEqual(Person.get_by(Person.firstname == 'Homer'), p1)
        self.assertEqual(Person.get_by(Person.firstname == 'Bart'), p2)
        self.assertEqual(Person.get_by(Person.firstname == 'Marge'), None)

        self.assertEqual(Person.get_by(Person.firstname == 'Homer',
                                       Person.surname == 'Simpson'), p1)
        self.assertEqual(Person.get_by(Person.firstname == 'Homer',
                                       Person.surname != 'Flanders'), p1)
        self.assertEqual(Person.get_by(Person.firstname != 'Bart',
                                       Person.surname != 'Flanders'), p1)
