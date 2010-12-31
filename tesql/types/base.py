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

from copy import deepcopy

import tesql

from tesql.disk.objects import BaseObject
from tesql.query import Filter


def exportedmethod (func, name=None, prefix='field_'):
    func._exported = True
    if not name:
        name = func.func_name.startswith(prefix) and \
               func.func_name[len(prefix):] or func.func_name
    func.func_name = name
    return staticmethod(func)

class BaseType (object):

    def __init__ (self):
        super(BaseType, self).__init__()
        self._outcoding = 'utf-8'
        self._incoding = 'utf-8'
        self._constraints = []
        self._data = None

    def __getstate__ (self):
        state = {
            'outcoding': self._outcoding,
            'data': deepcopy(self._data),
            'constraints': self._constraints,
        }

        return state

    def __setstate__ (self, state):
        self._outcoding = state['outcoding']
        self._data = state['data']
        self._constraints = state['constraints']

    @exportedmethod
    def field___eq__ (self, other):
        return Filter(lambda x: x.field_get(self.name) == other)

    @exportedmethod
    def field___ne__ (self, other):
        return Filter(lambda x: x.field_get(self.name) != other)

    def add_constraint (self, constraint):
        if 'item' in constraint.scope:
            self._constraints.append(constraint)

    def check_constraints (self, data):
        for constraint in self._constraints:
            if not constraint.check(data):
                raise ValueError("'%s' does not satisfies '%s' constraint." %
                                 (data, str(constraint)))

        return True

    def validate (self, data):
        self.check_constraints(data)

        return data

    def get_data (self, instance=None):
        return self._data

    def validate_data (self, instance=None):
        self.validate(self.get_data(instance=instance))

    def set_data (self, data, check=True, instance=None):
        if check:
            self._data = self.validate(data)
        else:
            self._data = data

    def clone (self):
        new = type(self)()
        new.__setstate__(self.__getstate__())

        return new

    def marshal (self):
        return unicode(self.get_data()).encode(self._outcoding)

    def unmarshal (self, value):
        return value.decode(self._incoding)


class BaseSortable (BaseType):

    def __init__ (self, *args, **kw):
        super(BaseSortable, self).__init__(*args, **kw)

    @exportedmethod
    def ascending (self, x, y):
        #return lambda x, y: cmp(x.field_get(self.name), y.field_get(self.name))
        return cmp(x.field_get(self.name), y.field_get(self.name))

    @exportedmethod
    def descending (self, x, y):
        #return lambda x, y: -cmp(x.field_get(self.name), y.field_get(self.name))
        return -cmp(x.field_get(self.name), y.field_get(self.name))

class BaseReference (BaseType):

    def __init__ (self, *args, **kw):
        super(BaseReference, self).__init__(*args, **kw)

        self.bind_to_entity(None)
        self.bind_to_inverse('')

    def __getstate__ (self):
        state = super(BaseReference, self).__getstate__()
        state['target'] = self._entity
        state['inverse'] = self._inverse

        return state

    def __setstate__ (self, state):
        super(BaseReference, self).__setstate__(state)

        self.bind_to_entity(state['target'])
        self.bind_to_inverse(state['inverse'])

    @exportedmethod
    def field_bind_to_entity (self, target):
        self._field.bind_to_entity(target)
        self._bound_entity = target

    @exportedmethod
    def field_bind_to_inverse (self, target):
        self._field.bind_to_inverse(target)

    def bind_to_entity (self, target):
        self._entity = target

    def bind_to_inverse (self, target):
        self._inverse = target


class BaseConstraint (object):

    def __init__ (self, constraint, entity=None, field_name=None):
        self._constraint = constraint
        self._entity = entity
        self._field_name = field_name

    def __str__ (self):
        return type(self).__name__


from tesql import __author__, __license__, __version__
