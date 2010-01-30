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

from tesql.types.constraints import ConstraintPositive
from tesql.types.constraints import ConstraintMin
from tesql.types.constraints import ConstraintMax
from tesql.types.constraints import ConstraintRequired


class TestIntegerConstraints (TestCase):

    def test_no_constraints (self):
        i = Integer()

        self.assertTrue(i.set_data(-12) == None)
        self.assertTrue(i.set_data(12) == None)
        self.assertTrue(i.set_data(1045) == None)

    def test_positive_constraint (self):
        i = Integer()
        i.add_constraint(ConstraintPositive(True))

        self.assertRaises(ValueError, i.set_data, -12)
        self.assertTrue(i.set_data(12) == None)
        self.assertTrue(i.set_data(1045) == None)

    def test_min_constraint (self):
        i = Integer()
        i.add_constraint(ConstraintMin(42))

        self.assertRaises(ValueError, i.set_data, -12)
        self.assertRaises(ValueError, i.set_data, 12)
        self.assertTrue(i.set_data(1045) == None)

    def test_max_constraint (self):
        i = Integer()
        i.add_constraint(ConstraintMax(42))

        self.assertTrue(i.set_data(-12) == None)
        self.assertTrue(i.set_data(12) == None)
        self.assertRaises(ValueError, i.set_data, 1045)

    def test_multiple_constraints (self):
        i = Integer()
        i.add_constraint(ConstraintPositive(True))
        i.add_constraint(ConstraintMax(42))

        self.assertRaises(ValueError, i.set_data, -12)
        self.assertTrue(i.set_data(12) == None)
        self.assertRaises(ValueError, i.set_data, 1045)

    def test_required_constraint (self):
        i = Integer()
        i.add_constraint(ConstraintRequired(True))

        self.assertRaises(ValueError, i.set_data, None)
        self.assertRaises(ValueError, i.set_data, 0)
        self.assertTrue(i.set_data(-12) == None)
        self.assertTrue(i.set_data(12) == None)
        self.assertTrue(i.set_data(1045) == None)

    def test_numeric_field (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)
            age = Field(Integer, positive=True, max=200)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')

        self.assertRaises(ValueError, Person, firstname='Marge',
                                              surname='Simpson', age=-1)
        self.assertRaises(ValueError, Person, firstname='Marge',
                                              surname='Simpson', age=512)
