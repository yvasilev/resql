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

from tesql.types.constraints import ConstraintLength
from tesql.types.constraints import ConstraintRequired


class TestStringConstraints (TestCase):

    def test_no_constraints (self):
        i = String()

        self.assertTrue(i.set_data('') == None)
        self.assertTrue(i.set_data('foo') == None)
        self.assertTrue(i.set_data('long foo bar') == None)

    def test_length_constraint (self):
        i = String()
        i.add_constraint(ConstraintLength(4))

        self.assertTrue(i.set_data('') == None)
        self.assertTrue(i.set_data('foo') == None)
        self.assertRaises(ValueError, i.set_data, 'long foo bar')

    def test_required_constraint (self):
        i = String()
        i.add_constraint(ConstraintRequired(True))

        self.assertRaises(ValueError, i.set_data, None)
        self.assertRaises(ValueError, i.set_data, '')
        self.assertTrue(i.set_data('foo') == None)
        self.assertTrue(i.set_data('long foo bar') == None)

    def test_string_field (self):
        class Person (Entity):
            firstname = Field(String, max_length=8)
            surname = Field(String)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')
        p2 = Person(firstname='Princess', surname='Kashmir')

        self.assertRaises(ValueError, Person, firstname='Jacqueline',
                                              surname='Bouvier')
        self.assertRaises(ValueError, Person, firstname='Bumblebee')

