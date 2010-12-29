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

import __builtin__

import tesql

from tesql.query import Filter

from base import BaseReference
from base import exportedmethod


class ReferenceOne (BaseReference):

    def __init__ (self, *args, **kw):
        super(ReferenceOne, self).__init__(*args, **kw)

        self.set_data(None, check=False)

    @exportedmethod
    def has (self, constraint, *constraints):
        for extra in constraints:
            constraint = constraint & extra

        return Filter(lambda x: constraint(x.field_get(self.name)))

    def get_data (self, instance=None):
        if super(ReferenceOne, self).get_data() == None:
            return None

        return tesql.orm.Session.default.get(self._entity,
                super(ReferenceOne, self).get_data())

    def set_data (self, value, check=True, instance=None):
        if not isinstance(value, tesql.orm.Entity):
            super(ReferenceOne, self).set_data(value, check)
        else:
            super(ReferenceOne, self).set_data(value.entity_pk_value, check)

    def marshal (self):
        return unicode(super(ReferenceOne, self).get_data()).encode(self._outcoding)

    def unmarshal (self, value):
        return self._entity.entity_pk.unmarshal(value)

class ReferenceMany (BaseReference):

    def __init__ (self, *args, **kw):
        super(ReferenceMany, self).__init__(*args, **kw)

        self.set_data([], check=False)

    def __len__ (self):
        return len(self._data)

    def __getitem__ (self, pos):
        # FIXME: Add support for slices
        return tesql.orm.Session.default.get(self._entity, self._data[pos])

    def __setitem__ (self, pos, instance):
        self._data.__setitem__(pos, self.validate(instance.entity_pk_value))

    def __delitem__ (self, pos):
        self._data.__delitem__(pos)

    def __iter__ (self):
        for pk in self._data:
            yield tesql.orm.Session.default.get(self._entity, pk)

    def __contains__ (self, instance):
        return self._data.__contains__(instance.entity_pk_value)

    def __eq__ (self, other):
        if len(self) != len(other):
            return False

        return all(self[i] == other[i] for i in xrange(len(self)))

    def eq (self, other):
        if len(self) != len(other):
            return False

        return all(self[i] == other[i] for i in xrange(len(self)))

    def __ne__ (self, other):
        return not self == other

    def append (self, value, check=True):
        if not isinstance(value, tesql.orm.Entity):
            pk = value
        else:
            pk = value.entity_pk_value

        if check:
            self._data.append(self.validate(pk))
        else:
            self._data.append(pk)

    def remove (self, value, check=True):
        if not isinstance(value, tesql.orm.Entity):
            pk = value
        else:
            pk = value.entity_pk_value

        self._data.remove(pk)

    @exportedmethod
    def any (self, constraint, *constraints):
        for extra in constraints:
            constraint = constraint & extra

        return Filter(lambda x: __builtin__.any(constraint(inst) for inst in \
                                    x.field_get(self.name)))

    @exportedmethod
    def all (self, constraint, *constraints):
        for extra in constraints:
            constraint = constraint & extra

        return Filter(lambda x: __builtin__.all(constraint(inst) for inst in \
                                    x.field_get(self.name)))

    @exportedmethod
    def contains (self, instance, *instances):
        return Filter(lambda x: __builtin__.all(inst in x.field_get(self.name) \
                                for inst in (instance,) + instances))

    def get_data (self, instance=None):
        return self

    def set_data (self, instances, check=True, instance=None):
        self._data = []
        for instance in instances:
            self.append(instance, check)

    def validate_data (self, instance=None):
        return None

    def marshal (self):
        return ', '.join(unicode(x).encode(self._outcoding) for x in self._data)

    def unmarshal (self, value):
        return [self._entity.entity_pk.unmarshal(x) for x in value.split(', ')]

class OneToOne (ReferenceOne):

    def __init__ (self, *args, **kw):
        super(OneToOne, self).__init__(*args, **kw)

    @exportedmethod
    def inverse_name (self, name):
        return name

    @exportedmethod
    def inverse_type (self):
        return QueryOneToOne


class ManyToOne (ReferenceOne):

    def __init__ (self, *args, **kw):
        super(ManyToOne, self).__init__(*args, **kw)

    @exportedmethod
    def inverse_name (self, name):
        return name + 's'

    @exportedmethod
    def inverse_type (self):
        return QueryManyToOne


class OneToMany (ReferenceMany):

    def __init__ (self, *args, **kw):
        super(OneToMany, self).__init__(*args, **kw)

    @exportedmethod
    def inverse_name (self, name):
        return name

    @exportedmethod
    def inverse_type (self):
        return QueryOneToMany


class ManyToMany (ReferenceMany):

    def __init__ (self, *args, **kw):
        super(ManyToMany, self).__init__(*args, **kw)

    @exportedmethod
    def inverse_name (self, name):
        return name + 's'

    @exportedmethod
    def inverse_type (self):
        return QueryManyToMany


class QueryOne (BaseReference):

    def __init__ (self, *args, **kw):
        super(QueryOne, self).__init__(*args, **kw)

    @exportedmethod
    def has (self, constraint, *constraints):
        for extra in constraints:
            constraint = constraint & extra

        return Filter(lambda x: constraint(x.field_get(self.name)))

    def validate_data (self, instance=None):
        return None

    def marshal (self):
        raise NotImplemented('You can not marshal a QueryOne Field.')

    def unmarshal (self, value):
        raise NotImplemented('You can not un-marshal a QueryOne Field.')

class QueryOneToOne (QueryOne):

    def __init__ (self, *args, **kw):
        super(QueryOneToOne, self).__init__(*args, **kw)

    def get_data (self, instance=None):
        return self._entity.get_by(getattr(self._entity, self._inverse) ==
                                   instance)

    def set_data (self, value, check=True, instance=None):
        value.field_set(self._inverse, instance, check=check)

class QueryOneToMany (BaseReference):

    def __init__ (self, *args, **kw):
        super(QueryOneToMany, self).__init__(*args, **kw)

    def get_data (self, instance=None):
        self._data = self._entity.get_by(
                getattr(self._entity, self._inverse).contains(instance))

        return self._data

    def set_data (self, value, check=True, instance=None):
        if self._data:
            getattr(self._data, self._inverse).remove(instance)

        if value:
            getattr(value, self._inverse).append(instance)

class QueryMany (BaseReference):

    def __init__ (self, *args, **kw):
        super(QueryMany, self).__init__(*args, **kw)

    def __len__ (self):
        return len(self._data)

    def __getitem__ (self, pos):
        # FIXME: Add support for slices
        return self._data.__getitem__(pos)

    def __iter__ (self):
        for target in self._data:
            yield target

    def __contains__ (self, target):
        return target in self._data

    def __eq__ (self, other):
        if len(self) != len(other):
            return False

        return sorted(list(self)) == sorted(list(other))

    def __ne__ (self, other):
        return not self == other

    @exportedmethod
    def any (self, constraint, *constraints):
        for extra in constraints:
            constraint = constraint & extra

        return Filter(lambda x: __builtin__.any(constraint(inst) for inst in \
                                    x.field_get(self.name)))

    @exportedmethod
    def all (self, constraint, *constraints):
        for extra in constraints:
            constraint = constraint & extra

        return Filter(lambda x: __builtin__.all(constraint(inst) for inst in \
                                    x.field_get(self.name)))

    @exportedmethod
    def contains (self, instance, *instances):
        return Filter(lambda x: __builtin__.all(inst in x.field_get(self.name) \
                                for inst in (instance,) + instances))

    def validate_data (self, instance=None):
        self._instance = instance

    def set_data (self, iterable, check=True, instance=None):
        self.get_data(instance=instance)

        while len(self._data):
            self.__delitem__(len(self._data) - 1)

        for target in iterable:
            self.append(target)

    def marshal (self):
        raise NotImplemented('You can not marshal a QueryOne Field.')

    def unmarshal (self, value):
        raise NotImplemented('You can not un-marshal a QueryOne Field.')

class QueryManyToOne (QueryMany):

    def __init__ (self, *args, **kw):
        super(QueryManyToOne, self).__init__(*args, **kw)

    def __setitem__ (self, pos, target):
        # FIXME: Add support for slices
        self.__delitem__(pos)

        if target:
            setattr(target, self._inverse, self._instance)

    def __delitem__ (self, pos):
        setattr(self.__getitem__(pos), self._inverse, None)
        self._data.__delitem__(pos)

    def append (self, target):
        setattr(target, self._inverse, self._instance)

    def get_data (self, instance=None):
        self._instance = instance

        self._data = self._entity.query.filter_by(
                    getattr(self._entity, self._inverse) == instance).all()

        return self


class QueryManyToMany (QueryMany):

    def __init__ (self, *args, **kw):
        super(QueryManyToMany, self).__init__(*args, **kw)

    def __setitem__ (self, pos, target):
        # FIXME: Add support for slices
        self.__delitem__(pos)

        if target:
            getattr(target, self._inverse).append(self._instance)

    def __delitem__ (self, pos):
        getattr(self.__getitem__(pos), self._inverse).remove(self._instance)
        self._data.__delitem__(pos)

    def append (self, target):
        getattr(target, self._inverse).append(self._instance)

    def get_data (self, instance=None):
        self._instance = instance

        self._data = self._entity.query.filter_by(
                    getattr(self._entity, self._inverse).contains(instance)).all()

        return self


from tesql import __author__, __license__, __version__
