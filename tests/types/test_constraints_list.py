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


import tesql

from tesql.types.constraints import init_constraints
from tesql.types.constraints import list_constraints

class TestConstraintsList (TestCase):

    def setUp (self):
        tesql.types.constraints.ALL_CONSTRAINTS = []

    def test_init_constraints (self):
        self.assertEqual(tesql.types.constraints.ALL_CONSTRAINTS, [])

        init_constraints()

        self.assertNotEqual(tesql.types.constraints.ALL_CONSTRAINTS, [])

    def test_list_constraints (self):
        self.assertEqual(tesql.types.constraints.ALL_CONSTRAINTS, [])

        list_constraints()

        self.assertNotEqual(tesql.types.constraints.ALL_CONSTRAINTS, [])
