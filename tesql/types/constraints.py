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

from inspect import getmodule, getmembers, isclass

import tesql

from base import BaseConstraint

ALL_CONSTRAINTS = []

def init_constraints ():
    global ALL_CONSTRAINTS

    ALL_CONSTRAINTS = []
    for cls in getmembers(getmodule(list_constraints), isclass):
        if issubclass(cls[1], BaseConstraint) and \
           hasattr(cls[1], 'argument'):
            ALL_CONSTRAINTS.append(cls[1])

def add_constraint (constraint):
    global ALL_CONSTRAINTS

    if not ALL_CONSTRAINTS:
        init_constraints()

    if issubclass(constraint, BaseConstraint) and \
       hasattr(constraint, 'argument'):
        ALL_CONSTRAINTS.append(cls[1])

def list_constraints ():
    global ALL_CONSTRAINTS

    if not ALL_CONSTRAINTS:
        init_constraints()

    return (x for x in ALL_CONSTRAINTS)


class ConstraintByFunction (BaseConstraint):

    def __init__ (self, function, entity=None, field_name=None):
        super(ConstraintByFunction, self).__init__(function, entity=entity,
                                                   field_name=field_name)

        self._scope = ('item',)

    def check (self, data):
        return self._constraint(data)

    @property
    def scope (self):
        return self._scope


class ConstraintLength (ConstraintByFunction):

    def __init__ (self, max_length, entity=None, field_name=None):
        super(ConstraintLength, self).__init__(lambda x: len(x) <= max_length,
                                        entity=entity, field_name=field_name)

    @staticmethod
    def argument ():
        return 'max_length'


class ConstraintMin (ConstraintByFunction):

    def __init__ (self, min_value, entity=None, field_name=None):
        super(ConstraintMin, self).__init__(lambda x: x >= min_value)

    @staticmethod
    def argument ():
        return 'min'


class ConstraintMax (ConstraintByFunction):

    def __init__ (self, max_value, entity=None, field_name=None):
        super(ConstraintMax, self).__init__(lambda x: x <= max_value,
                                        entity=entity, field_name=field_name)

    @staticmethod
    def argument ():
        return 'max'


class ConstraintPositive (ConstraintMin):

    def __init__ (self, value, entity=None, field_name=None):
        if value != True:
            raise ValueError(value)
        super(ConstraintPositive, self).__init__(0, entity=entity,
                                                    field_name=field_name)

    @staticmethod
    def argument ():
        return 'positive'

class ConstraintPrimaryKey (ConstraintByFunction):

    def __init__ (self, value, entity, field_name=None):
        if value not in [False, True]:
            raise ValueError("'%s' not a boolean" % value)

        super(ConstraintPrimaryKey, self).__init__(lambda x: not \
                tesql.orm.Session.default.has(entity, x))

        self._scope = value and ('item',) or ()

    @staticmethod
    def argument ():
        return 'primary_key'


class ConstraintUnique (ConstraintByFunction):

    def __init__ (self, value, entity, field_name):
        if value not in [False, True]:
            raise ValueError("'%s' not a boolean" % value)

        super(ConstraintUnique, self).__init__(lambda x: entity.get_by(
                getattr(entity, field_name) == x) == None, entity=entity,
                                                    field_name=field_name)

        self._scope = value and ('item',) or ()

    @staticmethod
    def argument ():
        return 'unique'


class ConstraintRequired (ConstraintByFunction):

    def __init__ (self, value, entity=None, field_name=None):
        if value not in [False, True]:
            raise ValueError("'%s' not a boolean" % value)

        super(ConstraintRequired, self).__init__(lambda x: bool(x),
                                        entity=entity, field_name=field_name)

        self._scope = value and ('item',) or ()

    @staticmethod
    def argument ():
        return 'required'


class ConstraintReferences (ConstraintByFunction):

    def __init__ (self, target, entity=None, field_name=None):
        super(ConstraintReferences, self).__init__(lambda x: x == None or \
                tesql.orm.Session.default.has(self._target, x),
                                        entity=entity, field_name=field_name)

        if isinstance(target, type) and issubclass(target, tesql.orm.Entity):
            self._target = target
        else:
            try:
                self._target = tesql.orm.Entity.get_entity_type_by_name(target)
            except KeyError:
                raise EnvironmentError("Waiting for '%s' to be defined" % target)

        if hasattr(getattr(entity, field_name), 'inverse_name'):
            inverse_name = getattr(entity, field_name).inverse_name(
                            entity.meta.name.lower())
            inverse_name = self._target.register_inverse(inverse_name,
                            getattr(entity, field_name).inverse_type(),
                            entity=entity, inverse=field_name, virtual=True)

        getattr(entity, field_name).bind_to_entity(self._target)

    @staticmethod
    def argument ():
        return 'entity'


class ConstraintInverse (ConstraintByFunction):

    def __init__ (self, target, entity=None, field_name=None):
        super(ConstraintInverse, self).__init__(lambda x: False)

        getattr(entity, field_name).bind_to_inverse(target)

        self._scope = ()

    @staticmethod
    def argument ():
        return 'inverse'


class ConstraintReadOnly (ConstraintByFunction):

    def __init__ (self, value, entity=None, field_name=None):
        if value not in [False, True]:
            raise ValueError("'%s' not a boolean" % value)

        super(ConstraintReadOnly, self).__init__(lambda x: False,
                                        entity=entity, field_name=field_name)

        self._scope = value and ('item',) or ()

    @staticmethod
    def argument ():
        return 'readonly'


class ConstraintChoices (ConstraintByFunction):

    def __init__ (self, value, entity=None, field_name=None):
        if not hasattr(value, '__iter__'):
            raise ValueError("'%s' not iterable" % value)

        super(ConstraintChoices, self).__init__(lambda x: x in value,
                                        entity=entity, field_name=field_name)

    @staticmethod
    def argument ():
        return 'choices'


from tesql import __author__, __license__, __version__
