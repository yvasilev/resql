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


from tesql.types import OneToOne
from tesql.types.base import BaseType
from tesql.types.constraints import list_constraints

from tesql.query import Filter


class Field (object):

    _position_counter = 0
    _subclasses = {}

    def __new__ (cls, field_type, *args, **kwargs):
        if not (isinstance(field_type, type) and issubclass(field_type,
                BaseType)) and not isinstance(field_type, BaseType):
            raise TypeError('Fields can only have types from resql.types.*')

        name = (isinstance(field_type, type) and field_type.__name__ or \
                    type(field_type).__name__) + Field.__name__

        if name not in Field._subclasses:
            Field._subclasses[name] = type(name, (Field,), {})
            field_type.register_methods(Field._subclasses[name])

        return super(Field, Field._subclasses[name]).__new__(
                        Field._subclasses[name])

    def __init__ (self, field_type, name=None, doc=None, **kwargs):
        self._position = Field._position_counter
        Field._position_counter += 1

        if isinstance(field_type, type) and issubclass(field_type, BaseType):
            self._field = field_type()
        elif isinstance(field_type, BaseType):
            self._field = field_type
        else: # pragma: no cover (not reachable, cached in __new__)
            raise TypeError('Fields can only have types from resql.types.*')

        self._primary_key = kwargs.get('primary_key', False)
        if self.is_primary_key:
            kwargs.pop('unique', None)

        self._virtual = kwargs.pop('virtual', False)
        self._autoincrement = kwargs.pop('autoincrement', False)
        self._default = kwargs.pop('default', None)

        self._singleton = self.is_primary_key and len(kwargs.get('choices', []))

        self._name = name

        self._kwargs = kwargs

    def __get__ (self, instance, entity=None):
        if instance:
            return instance.field_get(self.name)
        else:
            return self

    def __set__ (self, instance, value):
        return instance.field_set(self.name, value)

    def unmarshal (self, data):
        return self._field.unmarshal(data)

    @property
    def field (self):
        return self._field.clone()

    @property
    def default (self):
        return self._default

    @property
    def is_primary_key (self):
        return self._primary_key

    @property
    def is_foreign_key (self):
        return isinstance(self._field, OneToOne) and self.is_primary_key

    @property
    def foreign_key_entity (self):
        return self.is_foreign_key and self._bound_entity

    @property
    def is_virtual (self):
        return self._virtual

    @property
    def is_singleton (self):
        return self._singleton

    @property
    def is_autoincrementing (self):
        return self._autoincrement

    @property
    def is_constrained (self):
        return self.is_primary_key or any(x.argument() in self._kwargs for \
                                                    x in list_constraints())

    def constrain (self, entity):
        if not hasattr(self, '_pending_constraints'):
            self._pending_constraints = []

            for constraint in list_constraints():
                if constraint.argument() in self._kwargs:
                    self._pending_constraints.append([
                            constraint,
                            self._kwargs.get(constraint.argument()),
                            entity,
                            self.name])

        for constraint, value, entity, name in self._pending_constraints:
            try:
                self._field.add_constraint(constraint(value, entity=entity,
                        field_name=name))
            except EnvironmentError:
                pass
            else:
                self._pending_constraints.remove([constraint, value,
                                                  entity, name])

    @property
    def name (self):
        return self._name

    @property
    def field_name (self):
        return self._field_name

    def set_name (self, entity, name):
        self._name = self._name or name
        self._field_name = name


from tesql import __author__, __license__, __version__
