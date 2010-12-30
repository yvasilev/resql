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

from tesql.disk.strategies import Related

class TestSessionRelatedLoadStore (TestCase):

    def setUp (self):
        Entity.entities = {}
        self.path = '/tmp/test.tesqldb'
        Session(strategy=Related).be_default()
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
        Session().be_default()

    def test_session_cache_stack (self):
        class Person (Entity):
            pk = Field(Indexer, autoincrement=True, primary_key=True, virtual=True)
            firstname = Field(String)
            surname = Field(String)

        class Account (Entity):
            homedir = Field(String)
            person = Field(OneToOne, entity=Person, primary_key=True, virtual=True)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')

        a1 = Account(homedir='/home/hsimpson', person=p1)
        a2 = Account(homedir='/home/bsimpson', person=p2)

        self.assertTrue(Session.default._cache.contains(p1))
        self.assertTrue(Session.default._stack.contains(p1))
        self.assertTrue(Session.default._cache.contains(p2))
        self.assertTrue(Session.default._stack.contains(p2))

        self.assertTrue(Session.default._cache.contains(a1))
        self.assertTrue(Session.default._stack.contains(a1))
        self.assertTrue(Session.default._cache.contains(a2))
        self.assertTrue(Session.default._stack.contains(a2))

        self.assertTrue(('Person', 0) in Session.default._cache.keys())
        self.assertTrue(('Person', 1) in Session.default._cache.keys())
        self.assertTrue(('Account', 0) in Session.default._cache.keys())
        self.assertTrue(('Account', 1) in Session.default._cache.keys())
        self.assertEqual(len(Session.default._cache.keys()), 4)

        self.assertTrue(('Person', 0) in Session.default._stack.peek().keys())
        self.assertTrue(('Person', 1) in Session.default._stack.peek().keys())
        self.assertTrue(('Account', 0) in Session.default._stack.peek().keys())
        self.assertTrue(('Account', 1) in Session.default._stack.peek().keys())
        self.assertEqual(len(Session.default._stack.peek().keys()), 4)

        Session.default.commit()

        self.assertTrue(('Person', 0) in Session.default._cache.keys())
        self.assertTrue(('Person', 1) in Session.default._cache.keys())
        self.assertTrue(('Account', 0) in Session.default._cache.keys())
        self.assertTrue(('Account', 1) in Session.default._cache.keys())
        self.assertEqual(len(Session.default._cache.keys()), 4)

        self.assertEqual(Session.default._stack.peek().keys(), [])

        Session.default.expunge()

        self.assertEqual(Session.default._cache.keys(), [])
        self.assertEqual(Session.default._stack.peek().keys(), [])

    def test_session_store (self):
        class Person (Entity):
            pk = Field(Indexer, autoincrement=True, primary_key=True, virtual=True)
            firstname = Field(String)
            surname = Field(String)

        class Account (Entity):
            homedir = Field(String)
            person = Field(OneToOne, entity=Person, primary_key=True, virtual=True)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')

        a1 = Account(homedir='/home/hsimpson', person=p1)
        a2 = Account(homedir='/home/bsimpson', person=p2)

        self.assertTrue(Session.default._stack.contains(p1))
        self.assertTrue(Session.default._stack.contains(p2))
        self.assertTrue(Session.default._stack.contains(a1))
        self.assertTrue(Session.default._stack.contains(a2))

        self.assertFalse(os.path.isfile(os.path.join(self.path, 'Person', '0.conf')))
        self.assertFalse(os.path.isfile(os.path.join(self.path, 'Person', '1.conf')))
        self.assertFalse(os.path.isfile(os.path.join(self.path, 'Account', '0.conf')))
        self.assertFalse(os.path.isfile(os.path.join(self.path, 'Account', '1.conf')))

        Session.default.store(p1)
        Session.default.store(a2)

        self.assertFalse(Session.default._stack.contains(p1))
        self.assertFalse(Session.default._stack.contains(p2))
        self.assertFalse(Session.default._stack.contains(a1))
        self.assertFalse(Session.default._stack.contains(a2))

        self.assertTrue(os.path.isfile(os.path.join(self.path, 'Person', '0.conf')))
        self.assertTrue(os.path.isfile(os.path.join(self.path, 'Person', '1.conf')))
        self.assertFalse(os.path.isfile(os.path.join(self.path, 'Account', '0.conf')))
        self.assertFalse(os.path.isfile(os.path.join(self.path, 'Account', '1.conf')))

        self.assertEqual(open(os.path.join(self.path, 'Person', '0.conf'), 'rU').read(),
                         '\n[Person]\n\nfirstname: Homer\nsurname: Simpson\n'
                         '\n[Account]\n\nhomedir: /home/hsimpson\n')
        self.assertEqual(open(os.path.join(self.path, 'Person', '1.conf'), 'rU').read(),
                         '\n[Person]\n\nfirstname: Bart\nsurname: Simpson\n'
                         '\n[Account]\n\nhomedir: /home/bsimpson\n')

    def test_session_load (self):
        class Person (Entity):
            pk = Field(Indexer, autoincrement=True, primary_key=True, virtual=True)
            firstname = Field(String)
            surname = Field(String)

        class Account (Entity):
            homedir = Field(String)
            person = Field(OneToOne, entity=Person, primary_key=True, virtual=True)

        self.assertEqual(list(Session.default.list_primary_keys(Person)), [])
        self.assertEqual(list(Session.default.list_primary_keys(Account)), [])

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')

        a1 = Account(homedir='/home/hsimpson', person=p1)
        a2 = Account(homedir='/home/bsimpson', person=p2)

        Session.default.store(p1)
        Session.default.store(a2)

        self.assertTrue(os.path.isfile(os.path.join(self.path, 'Person', '0.conf')))
        self.assertTrue(os.path.isfile(os.path.join(self.path, 'Person', '1.conf')))

        Session.default.expunge()

        np1 = Session.default.get(Person, 0)
        np2 = Session.default.get(Person, 1)

        na1 = Session.default.get(Account, 0)
        na2 = Session.default.get(Account, 1)

        self.assertTrue(Session.default._cache.contains(np1))
        self.assertTrue(Session.default._cache.contains(np2))
        self.assertTrue(Session.default._cache.contains(na1))
        self.assertTrue(Session.default._cache.contains(na2))
        self.assertFalse(Session.default._stack.contains(np1))
        self.assertFalse(Session.default._stack.contains(np2))
        self.assertFalse(Session.default._stack.contains(na1))
        self.assertFalse(Session.default._stack.contains(na2))

        self.assertTrue(isinstance(np1, Person))
        self.assertEqual(np1.meta.name, 'Person')
        self.assertEqual(np1.pk, 0)
        self.assertEqual(np1.firstname, 'Homer')
        self.assertEqual(np1.surname, 'Simpson')

        self.assertTrue(isinstance(na1, Account))
        self.assertEqual(na1.meta.name, 'Account')
        self.assertEqual(na1.homedir, '/home/hsimpson')
        self.assertEqual(na1.person, np1)

        self.assertTrue(isinstance(np2, Person))
        self.assertEqual(np2.meta.name, 'Person')
        self.assertEqual(np2.pk, 1)
        self.assertEqual(np2.firstname, 'Bart')
        self.assertEqual(np2.surname, 'Simpson')

        self.assertTrue(isinstance(na2, Account))
        self.assertEqual(na2.meta.name, 'Account')
        self.assertEqual(na2.homedir, '/home/bsimpson')
        self.assertEqual(na2.person, np2)

    def test_session_get_from_cache (self):
        class Person (Entity):
            pk = Field(Indexer, autoincrement=True, primary_key=True, virtual=True)
            firstname = Field(String)
            surname = Field(String)

        class Account (Entity):
            homedir = Field(String)
            person = Field(OneToOne, entity=Person, primary_key=True, virtual=True)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')

        a1 = Account(homedir='/home/hsimpson', person=p1)
        a2 = Account(homedir='/home/bsimpson', person=p2)

        Session.default.commit()

        self.assertTrue(Session.default._cache.contains(p1))
        self.assertTrue(Session.default._cache.contains(p2))
        self.assertTrue(Session.default._cache.contains(a1))
        self.assertTrue(Session.default._cache.contains(a2))
        self.assertFalse(Session.default._stack.contains(p1))
        self.assertFalse(Session.default._stack.contains(p2))
        self.assertFalse(Session.default._stack.contains(a1))
        self.assertFalse(Session.default._stack.contains(a2))

        np1 = Session.default.get(Person, 0)
        np2 = Session.default.get(Person, 1)

        na1 = Session.default.get(Account, 0)
        na2 = Session.default.get(Account, 1)

        self.assertTrue(Session.default._cache.contains(np1))
        self.assertTrue(Session.default._cache.contains(np2))
        self.assertTrue(Session.default._cache.contains(na1))
        self.assertTrue(Session.default._cache.contains(na2))
        self.assertFalse(Session.default._stack.contains(np1))
        self.assertFalse(Session.default._stack.contains(np2))
        self.assertFalse(Session.default._stack.contains(na1))
        self.assertFalse(Session.default._stack.contains(na2))

        self.assertTrue(isinstance(np1, Person))
        self.assertEqual(np1.meta.name, 'Person')
        self.assertEqual(np1.pk, 0)
        self.assertEqual(np1.firstname, 'Homer')
        self.assertEqual(np1.surname, 'Simpson')

        self.assertTrue(isinstance(na1, Account))
        self.assertEqual(na1.meta.name, 'Account')
        self.assertEqual(na1.homedir, '/home/hsimpson')

        self.assertTrue(isinstance(np2, Person))
        self.assertEqual(np2.meta.name, 'Person')
        self.assertEqual(np2.pk, 1)
        self.assertEqual(np2.firstname, 'Bart')
        self.assertEqual(np2.surname, 'Simpson')

        self.assertTrue(isinstance(na2, Account))
        self.assertEqual(na2.meta.name, 'Account')
        self.assertEqual(na2.homedir, '/home/bsimpson')

    def test_session_get_from_disk (self):
        class Person (Entity):
            pk = Field(Indexer, autoincrement=True, primary_key=True, virtual=True)
            firstname = Field(String)
            surname = Field(String)

        class Account (Entity):
            homedir = Field(String)
            person = Field(OneToOne, entity=Person, primary_key=True, virtual=True)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')

        a1 = Account(homedir='/home/hsimpson', person=p1)
        a2 = Account(homedir='/home/bsimpson', person=p2)

        Session.default.commit()
        Session.default.expunge()

        self.assertFalse(Session.default._cache)

        np1 = Session.default.get(Person, 0)
        np2 = Session.default.get(Person, 1)

        na1 = Session.default.get(Account, 0)
        na2 = Session.default.get(Account, 1)

        self.assertTrue(Session.default._cache.contains(np1))
        self.assertTrue(Session.default._cache.contains(np2))
        self.assertTrue(Session.default._cache.contains(na1))
        self.assertTrue(Session.default._cache.contains(na2))
        self.assertFalse(Session.default._stack.contains(np1))
        self.assertFalse(Session.default._stack.contains(np2))
        self.assertFalse(Session.default._stack.contains(na1))
        self.assertFalse(Session.default._stack.contains(na2))

        self.assertTrue(isinstance(np1, Person))
        self.assertEqual(np1.meta.name, 'Person')
        self.assertEqual(np1.pk, 0)
        self.assertEqual(np1.firstname, 'Homer')
        self.assertEqual(np1.surname, 'Simpson')

        self.assertTrue(isinstance(na1, Account))
        self.assertEqual(na1.meta.name, 'Account')
        self.assertEqual(na1.homedir, '/home/hsimpson')

        self.assertTrue(isinstance(np2, Person))
        self.assertEqual(np2.meta.name, 'Person')
        self.assertEqual(np2.pk, 1)
        self.assertEqual(np2.firstname, 'Bart')
        self.assertEqual(np2.surname, 'Simpson')

        self.assertTrue(isinstance(na2, Account))
        self.assertEqual(na2.meta.name, 'Account')
        self.assertEqual(na2.homedir, '/home/bsimpson')

    def test_session_store_recursive (self):
        class Person (Entity):
            pk = Field(Indexer, autoincrement=True, primary_key=True, virtual=True)
            firstname = Field(String)
            surname = Field(String)

        class Account (Entity):
            homedir = Field(String)
            person = Field(OneToOne, entity=Person, primary_key=True, virtual=True)

        class Quota (Entity):
            size = Field(Integer, default=100000)
            account = Field(OneToOne, entity=Account, primary_key=True, virtual=True)

        p1 = Person(firstname='Homer', surname='Simpson')
        p2 = Person(firstname='Bart', surname='Simpson')

        a1 = Account(homedir='/home/hsimpson', person=p1)
        a2 = Account(homedir='/home/bsimpson', person=p2)

        q1 = Quota(account=a1)
        q2 = Quota(size=200000, account=a2)

        self.assertTrue(Session.default._stack.contains(p1))
        self.assertTrue(Session.default._stack.contains(p2))
        self.assertTrue(Session.default._stack.contains(a1))
        self.assertTrue(Session.default._stack.contains(a2))
        self.assertTrue(Session.default._stack.contains(q1))
        self.assertTrue(Session.default._stack.contains(q2))

        self.assertFalse(os.path.isfile(os.path.join(self.path, 'Person', '0.conf')))
        self.assertFalse(os.path.isfile(os.path.join(self.path, 'Person', '1.conf')))
        self.assertFalse(os.path.isfile(os.path.join(self.path, 'Account', '0.conf')))
        self.assertFalse(os.path.isfile(os.path.join(self.path, 'Account', '1.conf')))
        self.assertFalse(os.path.isfile(os.path.join(self.path, 'Quota', '0.conf')))
        self.assertFalse(os.path.isfile(os.path.join(self.path, 'Quota', '1.conf')))

        Session.default.store(p1)
        Session.default.store(a2)

        self.assertFalse(Session.default._stack.contains(p1))
        self.assertFalse(Session.default._stack.contains(p2))
        self.assertFalse(Session.default._stack.contains(a1))
        self.assertFalse(Session.default._stack.contains(a2))
        self.assertFalse(Session.default._stack.contains(q1))
        self.assertFalse(Session.default._stack.contains(q2))

        self.assertTrue(os.path.isfile(os.path.join(self.path, 'Person', '0.conf')))
        self.assertTrue(os.path.isfile(os.path.join(self.path, 'Person', '1.conf')))
        self.assertFalse(os.path.isfile(os.path.join(self.path, 'Account', '0.conf')))
        self.assertFalse(os.path.isfile(os.path.join(self.path, 'Account', '1.conf')))
        self.assertFalse(os.path.isfile(os.path.join(self.path, 'Quota', '0.conf')))
        self.assertFalse(os.path.isfile(os.path.join(self.path, 'Quota', '1.conf')))

        self.assertEqual(open(os.path.join(self.path, 'Person', '0.conf'), 'rU').read(),
                         '\n[Person]\n\nfirstname: Homer\nsurname: Simpson\n'
                         '\n[Account]\n\nhomedir: /home/hsimpson\n'
                         '\n[Quota]\n\nsize: 100000\n')
        self.assertEqual(open(os.path.join(self.path, 'Person', '1.conf'), 'rU').read(),
                         '\n[Person]\n\nfirstname: Bart\nsurname: Simpson\n'
                         '\n[Account]\n\nhomedir: /home/bsimpson\n'
                         '\n[Quota]\n\nsize: 200000\n')
