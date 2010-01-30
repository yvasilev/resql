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

class TestQueryRelations (TestCase):

    def setUp (self):
        self.path = '/tmp/test.tesqldb'
        Session.default.bind(self.path)
        Session.default.expunge()
        if os.path.lexists(self.path):  # pragma: no cover
            raise EnvironmentError("Unable to run tests because temporary "
                                   "dir '%s' exists" % self.path)

    def tearDown (self):
        if os.path.lexists(self.path):
            for dirpath, dirnames, filenames in os.walk(self.path, topdown=False):
                for name in filenames:
                    os.unlink(os.path.join(dirpath, name))

                for name in dirnames:
                    os.rmdir(os.path.join(dirpath, name))

            os.rmdir(self.path)

    def test_referenceone_eq_from_memory (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        class Account (Entity):
            homedir = Field(String)
            person = Field(OneToOne, entity=Person)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')
        p3 = Person(firstname='Ned', surname='Flanders')

        a1 = Account(homedir='/home/hsimpson', person=p1)
        a2 = Account(homedir='/home/bsimpson', person=p2)
        a3 = Account(homedir='/home/nflanders', person=p3)

        self.assertEqual(Account.get_by(Account.person == p1), a1)
        self.assertEqual(Account.get_by(Account.person == p2), a2)
        self.assertEqual(Account.get_by(Account.person == p3), a3)

    def test_referenceone_eq_from_disk (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        class Account (Entity):
            homedir = Field(String)
            person = Field(OneToOne, entity=Person)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')
        p3 = Person(firstname='Ned', surname='Flanders')

        a1 = Account(homedir='/home/hsimpson', person=p1)
        a2 = Account(homedir='/home/bsimpson', person=p2)
        a3 = Account(homedir='/home/nflanders', person=p3)

        Session.default.commit()
        Session.default.expunge()

        self.assertEqual(Account.get_by(Account.person == p1), a1)
        self.assertEqual(Account.get_by(Account.person == p2), a2)
        self.assertEqual(Account.get_by(Account.person == p3), a3)

    def test_referenceone_eq_from_mixed (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        class Account (Entity):
            homedir = Field(String)
            person = Field(OneToOne, entity=Person)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')

        a1 = Account(homedir='/home/hsimpson', person=p1)

        Session.default.commit()
        Session.default.expunge()

        p3 = Person(firstname='Ned', surname='Flanders')

        a2 = Account(homedir='/home/bsimpson', person=p2)
        a3 = Account(homedir='/home/nflanders', person=p3)

        self.assertEqual(Account.get_by(Account.person == p1), a1)
        self.assertEqual(Account.get_by(Account.person == p2), a2)
        self.assertEqual(Account.get_by(Account.person == p3), a3)

    def test_referenceone_ne_from_memory (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        class Account (Entity):
            homedir = Field(String)
            person = Field(OneToOne, entity=Person)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')

        a1 = Account(homedir='/home/hsimpson', person=p1)
        a2 = Account(homedir='/home/bsimpson', person=p2)

        self.assertEqual(Account.get_by(Account.person != p1), a2)
        self.assertEqual(Account.get_by(Account.person != p2), a1)

    def test_referenceone_ne_from_disk (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        class Account (Entity):
            homedir = Field(String)
            person = Field(OneToOne, entity=Person)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')

        a1 = Account(homedir='/home/hsimpson', person=p1)
        a2 = Account(homedir='/home/bsimpson', person=p2)

        Session.default.commit()
        Session.default.expunge()

        self.assertEqual(Account.get_by(Account.person != p1), a2)
        self.assertEqual(Account.get_by(Account.person != p2), a1)

    def test_referenceone_ne_from_mixed (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        class Account (Entity):
            homedir = Field(String)
            person = Field(OneToOne, entity=Person)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')

        a1 = Account(homedir='/home/hsimpson', person=p1)

        Session.default.commit()
        Session.default.expunge()

        a2 = Account(homedir='/home/bsimpson', person=p2)

        self.assertEqual(Account.get_by(Account.person != p1), a2)
        self.assertEqual(Account.get_by(Account.person != p2), a1)

    def test_referenceone_has_from_memory (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        class Account (Entity):
            homedir = Field(String)
            person = Field(OneToOne, entity=Person)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')
        p3 = Person(firstname='Ned', surname='Flanders')

        a1 = Account(homedir='/home/hsimpson', person=p1)
        a2 = Account(homedir='/home/bsimpson', person=p2)
        a3 = Account(homedir='/home/nflanders', person=p3)

        self.assertEqual(Account.get_by(Account.person.has( \
                Person.firstname == 'Homer')), a1)
        self.assertEqual(Account.get_by(Account.person.has( \
                Person.firstname == 'Bart')), a2)
        self.assertEqual(Account.get_by(Account.person.has( \
                Person.firstname == 'Ned')), a3)

        self.assertEqual(Account.get_by(Account.person.has( \
                Person.surname == 'Simpson') & Account.person.has( \
                Person.firstname == 'Bart')), a2)

        self.assertEqual(Account.get_by(Account.person.has( \
                Person.surname == 'Simpson') & Account.homedir.contains('b')), a2)

    def test_referenceone_has_from_disk (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        class Account (Entity):
            homedir = Field(String)
            person = Field(OneToOne, entity=Person)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')
        p3 = Person(firstname='Ned', surname='Flanders')

        a1 = Account(homedir='/home/hsimpson', person=p1)
        a2 = Account(homedir='/home/bsimpson', person=p2)
        a3 = Account(homedir='/home/nflanders', person=p3)

        Session.default.commit()
        Session.default.expunge()

        self.assertEqual(Account.get_by(Account.person.has( \
                Person.firstname == 'Homer')), a1)
        self.assertEqual(Account.get_by(Account.person.has( \
                Person.firstname == 'Bart')), a2)
        self.assertEqual(Account.get_by(Account.person.has( \
                Person.firstname == 'Ned')), a3)

        self.assertEqual(Account.get_by(Account.person.has( \
                Person.surname == 'Simpson') & Account.person.has( \
                Person.firstname == 'Bart')), a2)

        self.assertEqual(Account.get_by(Account.person.has( \
                Person.surname == 'Simpson') & Account.homedir.contains('b')), a2)

    def test_referenceone_has_from_mixed (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        class Account (Entity):
            homedir = Field(String)
            person = Field(OneToOne, entity=Person)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')

        a1 = Account(homedir='/home/hsimpson', person=p1)

        Session.default.commit()
        Session.default.expunge()

        p3 = Person(firstname='Ned', surname='Flanders')

        a2 = Account(homedir='/home/bsimpson', person=p2)
        a3 = Account(homedir='/home/nflanders', person=p3)

        self.assertEqual(Account.get_by(Account.person.has( \
                Person.firstname == 'Homer')), a1)
        self.assertEqual(Account.get_by(Account.person.has( \
                Person.firstname == 'Bart')), a2)
        self.assertEqual(Account.get_by(Account.person.has( \
                Person.firstname == 'Ned')), a3)

        self.assertEqual(Account.get_by(Account.person.has( \
                Person.surname == 'Simpson') & Account.person.has( \
                Person.firstname == 'Bart')), a2)

        self.assertEqual(Account.get_by(Account.person.has( \
                Person.surname == 'Simpson') & Account.homedir.contains('b')), a2)

    def test_referencemany_eq_from_memory (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        class Home (Entity):
            address = Field(String)
            person = Field(OneToMany, entity=Person)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')
        p3 = Person(firstname='Ned', surname='Flanders')

        h1 = Home(address='742 Evergreen', person=[p1, p2])
        h2 = Home(address='744 Evergreen', person=[p3])

        self.assertEqual(Home.get_by(Home.person == [p1, p2]), h1)
        self.assertEqual(Home.get_by(Home.person == [p3]), h2)

    def test_referencemany_eq_from_disk (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        class Home (Entity):
            address = Field(String)
            person = Field(OneToMany, entity=Person)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')
        p3 = Person(firstname='Ned', surname='Flanders')

        h1 = Home(address='742 Evergreen', person=[p1, p2])
        h2 = Home(address='744 Evergreen', person=[p3])

        Session.default.commit()
        Session.default.expunge()

        self.assertEqual(Home.get_by(Home.person == [p1, p2]), h1)
        self.assertEqual(Home.get_by(Home.person == [p3]), h2)

    def test_referencemany_eq_from_mixed (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        class Home (Entity):
            address = Field(String)
            person = Field(OneToMany, entity=Person)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')

        h1 = Home(address='742 Evergreen', person=[p1, p2])

        Session.default.commit()
        Session.default.expunge()

        p3 = Person(firstname='Ned', surname='Flanders')

        h2 = Home(address='744 Evergreen', person=[p3])

        self.assertEqual(Home.get_by(Home.person == [p1, p2]), h1)
        self.assertEqual(Home.get_by(Home.person == [p3]), h2)

    def test_referencemany_ne_from_memory (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        class Home (Entity):
            address = Field(String)
            person = Field(OneToMany, entity=Person)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')
        p3 = Person(firstname='Ned', surname='Flanders')

        h1 = Home(address='742 Evergreen', person=[p1, p2])
        h2 = Home(address='744 Evergreen', person=[p3])

        self.assertEqual(Home.get_by(Home.person != [p1, p2]), h2)
        self.assertEqual(Home.get_by(Home.person != [p3]), h1)

    def test_referencemany_ne_from_disk (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        class Home (Entity):
            address = Field(String)
            person = Field(OneToMany, entity=Person)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')
        p3 = Person(firstname='Ned', surname='Flanders')

        h1 = Home(address='742 Evergreen', person=[p1, p2])
        h2 = Home(address='744 Evergreen', person=[p3])

        Session.default.commit()
        Session.default.expunge()

        self.assertEqual(Home.get_by(Home.person != [p1, p2]), h2)
        self.assertEqual(Home.get_by(Home.person != [p3]), h1)

    def test_referencemany_ne_from_mixed (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        class Home (Entity):
            address = Field(String)
            person = Field(OneToMany, entity=Person)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')

        h1 = Home(address='742 Evergreen', person=[p1, p2])

        Session.default.commit()
        Session.default.expunge()

        p3 = Person(firstname='Ned', surname='Flanders')

        h2 = Home(address='744 Evergreen', person=[p3])

        self.assertEqual(Home.get_by(Home.person != [p1, p2]), h2)
        self.assertEqual(Home.get_by(Home.person != [p3]), h1)

    def test_referencemany_contains_from_memory (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        class Home (Entity):
            address = Field(String)
            person = Field(OneToMany, entity=Person)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')
        p3 = Person(firstname='Ned', surname='Flanders')

        h1 = Home(address='742 Evergreen', person=[p1, p2])
        h2 = Home(address='744 Evergreen', person=[p3])

        self.assertEqual(Home.get_by(Home.person.contains(p1)), h1)
        self.assertEqual(Home.get_by(Home.person.contains(p2)), h1)
        self.assertEqual(Home.get_by(Home.person.contains(p1, p2)), h1)
        self.assertEqual(Home.get_by(Home.person.contains(p3)), h2)

    def test_referencemany_contains_from_disk (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        class Home (Entity):
            address = Field(String)
            person = Field(OneToMany, entity=Person)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')
        p3 = Person(firstname='Ned', surname='Flanders')

        h1 = Home(address='742 Evergreen', person=[p1, p2])
        h2 = Home(address='744 Evergreen', person=[p3])

        Session.default.commit()
        Session.default.expunge()

        self.assertEqual(Home.get_by(Home.person.contains(p1)), h1)
        self.assertEqual(Home.get_by(Home.person.contains(p2)), h1)
        self.assertEqual(Home.get_by(Home.person.contains(p1, p2)), h1)
        self.assertEqual(Home.get_by(Home.person.contains(p3)), h2)

    def test_referencemany_contains_from_mixed (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        class Home (Entity):
            address = Field(String)
            person = Field(OneToMany, entity=Person)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')

        h1 = Home(address='742 Evergreen', person=[p1, p2])

        Session.default.commit()
        Session.default.expunge()

        p3 = Person(firstname='Ned', surname='Flanders')

        h2 = Home(address='744 Evergreen', person=[p3])

        self.assertEqual(Home.get_by(Home.person.contains(p1)), h1)
        self.assertEqual(Home.get_by(Home.person.contains(p2)), h1)
        self.assertEqual(Home.get_by(Home.person.contains(p1, p2)), h1)
        self.assertEqual(Home.get_by(Home.person.contains(p3)), h2)

    def test_referencemany_any_from_memory (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        class Home (Entity):
            address = Field(String)
            person = Field(OneToMany, entity=Person)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')
        p3 = Person(firstname='Ned', surname='Flanders')

        h1 = Home(address='742 Evergreen', person=[p1, p2])
        h2 = Home(address='744 Evergreen', person=[p3])

        self.assertEqual(Home.get_by(Home.person.any(Person.firstname == \
                         'Homer')), h1)
        self.assertEqual(Home.get_by(Home.person.any(Person.firstname == \
                         'Bart')), h1)
        self.assertEqual(Home.get_by(Home.person.any(Person.firstname == \
                         'Ned')), h2)

    def test_referencemany_any_from_disk (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        class Home (Entity):
            address = Field(String)
            person = Field(OneToMany, entity=Person)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')
        p3 = Person(firstname='Ned', surname='Flanders')

        h1 = Home(address='742 Evergreen', person=[p1, p2])
        h2 = Home(address='744 Evergreen', person=[p3])

        Session.default.commit()
        Session.default.expunge()

        self.assertEqual(Home.get_by(Home.person.any(Person.firstname == \
                         'Homer')), h1)
        self.assertEqual(Home.get_by(Home.person.any(Person.firstname == \
                         'Bart')), h1)
        self.assertEqual(Home.get_by(Home.person.any(Person.firstname == \
                         'Ned')), h2)

    def test_referencemany_any_from_mixed (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        class Home (Entity):
            address = Field(String)
            person = Field(OneToMany, entity=Person)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')

        h1 = Home(address='742 Evergreen', person=[p1, p2])

        Session.default.commit()
        Session.default.expunge()

        p3 = Person(firstname='Ned', surname='Flanders')

        h2 = Home(address='744 Evergreen', person=[p3])

        self.assertEqual(Home.get_by(Home.person.any(Person.firstname == \
                         'Homer')), h1)
        self.assertEqual(Home.get_by(Home.person.any(Person.firstname == \
                         'Bart')), h1)
        self.assertEqual(Home.get_by(Home.person.any(Person.firstname == \
                         'Ned')), h2)

    def test_referencemany_all_from_memory (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        class Home (Entity):
            address = Field(String)
            person = Field(OneToMany, entity=Person)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')
        p3 = Person(firstname='Ned', surname='Flanders')

        h1 = Home(address='742 Evergreen', person=[p1, p2])
        h2 = Home(address='744 Evergreen', person=[p3])

        self.assertEqual(Home.get_by(Home.person.all(Person.surname == \
                         'Simpson')), h1)
        self.assertEqual(Home.get_by(Home.person.all(Person.surname == \
                         'Flanders')), h2)

    def test_referencemany_all_from_disk (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        class Home (Entity):
            address = Field(String)
            person = Field(OneToMany, entity=Person)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')
        p3 = Person(firstname='Ned', surname='Flanders')

        h1 = Home(address='742 Evergreen', person=[p1, p2])
        h2 = Home(address='744 Evergreen', person=[p3])

        Session.default.commit()
        Session.default.expunge()

        self.assertEqual(Home.get_by(Home.person.all(Person.surname == \
                         'Simpson')), h1)
        self.assertEqual(Home.get_by(Home.person.all(Person.surname == \
                         'Flanders')), h2)

    def test_referencemany_all_from_mixed (self):
        class Person (Entity):
            firstname = Field(String)
            surname = Field(String)

        class Home (Entity):
            address = Field(String)
            person = Field(OneToMany, entity=Person)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')

        h1 = Home(address='742 Evergreen', person=[p1, p2])

        Session.default.commit()
        Session.default.expunge()

        p3 = Person(firstname='Ned', surname='Flanders')

        h2 = Home(address='744 Evergreen', person=[p3])

        self.assertEqual(Home.get_by(Home.person.all(Person.surname == \
                         'Simpson')), h1)
        self.assertEqual(Home.get_by(Home.person.all(Person.surname == \
                         'Flanders')), h2)
