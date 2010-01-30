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

"""
tesql's object object oriented interface

This package contains the classes needed to provide an object oriented
interface to a tesql database. Starting from a table (Entity) and a
column (Field) abstractions and going up to session management via the
Session class and the Session.default object.  It also includes some handy
decorators that allow for easy setting of extra table/entity options.

This package is safe for 'from tesql.orm import *'

It contains the following classes:

Session: an in-memory cache of all the rows/instances created, loaded
    and modified by the program. It also supports (non atomic) commits
    and rollbacks of the modified instances.

    It provides a special class property (Session.default) containing
    the currently used Session object.

Entity: the super-class from which all tesql tables have to be derived.

    It provides a special class property (Derived.query) that generates
    a Query object associated with the entity, as well as, some class
    methods providing a shortcut for querying entity's instances by
    primary key (Derived.get(...)) and by fields (Derived.get_by(...)).

Field: provides the functionality needed to use/link a data type from
    orm.types as an entity column.  When instantiated, it is passed the
    data type the field will have as the first argument and the actual
    Field instance that will be created will be of a dynamically created
    subtype of Field tailored for the specific data type it'll host.

It has the following sub packages:
decorators - used to set some options for entities
entity     - provides the Entity class
field      - provides the Field class
session    - provides the Session class

Examples:

>>> from tesql.types import *
>>> from tesql.orm import *
>>>
>>> class Person (Entity):
...     firstname = Field(String, required=True)
...     surname = Field(String, required=True)
...
>>> class Account (Entity):
...     login = Field(String, primary_key=True)
...     person = Field(OneToOne, entity=Person)
...
>>> homer = Person(firstname='Homer', surname='Simpson')
>>> hacc = Account(login='hsimpson', person=homer)
>>> hacc.person == homer
True
>>> homer.account == hacc
True
>>> Person.get_by(Person.account.has(Account.login.contains('simpson'))
...              ).firstname
'Homer'

"""

from tesql.orm.session import Session
from tesql.orm.field import Field
from tesql.orm.entity import Entity

__all__ = ['Field', 'Entity', 'Session']


from tesql import __author__, __license__, __version__
