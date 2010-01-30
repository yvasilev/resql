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
Text based SQL like backend with a nice object oriented interface

This is a pure python implementation of a relational database that uses
plain text files to store the information.  The exact way the information
is stored can be customized on a per table/entity level, defaulting to
storing each row in a separate RFC 2822 type .conf file inside a directory
named after the table/entity name.

The database supports many of the expected features that a modern ORM
should provide and has some special optimizations for usage as a
configuration system for any project.  This is done by mapping an entity
to a file (rather than to a directory) and defining it in a way that it
can have only one row.

It has the following sub packages:
disk  - on disk format and storage strategies
orm   - object oriented interface to the database
query - mechanisms used to do queries on the database
types - data types usable as columns/fields

Examples:

Using tesql as a normal database:

>>> from tesql.types import *
>>> from tesql.orm import *
>>>
>>> class Person (Entity):
...     firstname = Field(String)
...     surname = Field(String)
>>>
>>> homer = Person(firstname='Homer', surname='Simpson')

Using tesql as a cofiguration system:

>>> from tesql.types import *
>>> from tesql.orm import *
>>> from tesql.orm.decorators import location
>>>
>>> @location('/etc/package.conf')  # python >= 2.6
... class Settings (Entity):
...     pk = Field(Integer, choices=[0], primary_key=True, virtual=True)
...     user = Field(String)

>>> Settings = location('/etc/package.conf')(Settings)  # python < 2.6

"""


__author__ = "Yuri Vasilevski <yvasilev@gentoo.org>"
__copyright__ = "Copyright 2010 - Yuri Vasilevski"
__license__ = "GPL-3"

__status__ = "Development"
__version__ = "0.0.0"
__version_info__ = (0, 0, 0)
