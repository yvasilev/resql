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
Useful decorators for changing some entity options

This package contains class decorators designed to decorate tables/entities
inherited from the Entity class.  They are used to alter some behavior of
the entity you are defining, like where the actual data for that entity
will be stored to; or what strategy will be used to store the data.

It contains the following decorators:

options: the general purpose decorator, with it you can set several options
    at once specifying them as keyword arguments.

location: to set the storage location for an entity.

Examples:

Using an entity as a configuration storage via location decorator:

>>> from tesql.types import *
>>> from tesql.orm import *
>>>
>>> @location('/etc/foo.conf')  # python >= 2.6
... class Settings (Entity):
...     pk = Field(Integer, choices=[0], primary_key=True, virtual=True)
...     path = Field(String)
...
>>> Settings = location('/etc/foo.conf')(Settings)  # python < 2.6

Using an entity as a configuration storage via options decorator:

>>> from tesql.types import *
>>> from tesql.orm import *
>>>
>>> @options(location='/etc/foo.conf')  # python >= 2.6
... class Settings (Entity):
...     pk = Field(Integer, choices=[0], primary_key=True, virtual=True)
...     path = Field(String)
...
>>> Settings = options(location='/etc/foo.conf')(Settings)  # python < 2.6

"""

from tesql.orm import Session


def options (strategy=None, location=None):
    """This decorator sets different options of an entity depending on which
    keyword arguments are passed to it. For the exact description of how
    the different keyword arguments affect the entity see the descriptions
    of the decorators named after each keyword argument.
    """

    def options_decorator (cls):
        # FIXME: Add support for changing strategies
        if location:
            Session.default.bind_entity(cls, location)

        return cls

    return options_decorator

def location (path):
    """This decorator sets the location of where the data will be stored.

    With it you can control different aspects of where the data will be
    stored depending on two things: the path parameter and some properties
    of the entity it will decorate.

    It follows the following rules:
    - if path is absolute, it uses that path.
    - if path is relative, it prepend it with the base path of the db.
    - if entity is a singleton, it uses the path as a filename.
    - if entity is not a singleton and path is a string, it uses it to
      specify the directory to store columns as files.
    - if entity is not a singleton and path is a dictionary, it uses it
      store columns in the specified files if the column's primary key
      is in the dictionary, or to the directory specified accessible by
      the key None if present in path, or to the default location if
      None is not in path.
    """
    return options(location=path)


from tesql import __author__, __license__, __version__
