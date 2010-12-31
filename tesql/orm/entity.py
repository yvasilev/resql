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


from tesql.disk.objects import make_object
from tesql.disk.objects import BaseObject

from tesql.orm import Field
from tesql.orm import Session

from tesql.types import Indexer

from tesql.query import Query

class EntityMeta (type):

    entities = {}

    def __init__ (cls, name, bases, ns):
        super(EntityMeta, cls).__init__(name, bases, ns)

        cls._fields = {}
        cls._pk_name = None
        cls._constrained = False

        cls._register_entity()

        for key, value in ns.items():
            if isinstance(value, Field):
                cls._register_field(key, value)

        if not cls._pk_name:
            setattr(cls, 'pk', Field(Indexer, primary_key=True, autoincrement=True))
            cls._register_field('pk', getattr(cls, 'pk'))
            cls.meta.pk._position = -1

        cls._field_order = tuple(k for k, o in sorted([(x, v._position)
                for x, v in cls._fields.iteritems()], lambda x, y: x[1] - y[1]))

        for entity in cls.entities.itervalues():
            entity._constraint_fields()

    def _register_field (cls, name, field):
        # FIXME: Set docstring to 'doc' argument of field
        #        plus text representation of the restrictions.
        field.set_name(cls, name)
        cls._fields[field.name] = field

        if cls._fields[field.name].is_constrained:
            field.constrain(cls)

        if cls._fields[field.name].is_primary_key:
            if cls._pk_name:
                raise AttributeError('Only one primary_key per Entity alowed.')
            cls._pk_name = field.name
        elif field.name is 'pk':
            raise AttributeError('"pk" field name is reserved for primary keys')

    def _constraint_fields (cls):
        for field in cls._fields.itervalues():
            if cls._fields[field.name].is_constrained:
                field.constrain(cls)

    def _register_entity (cls):
        cls._entity_name = cls.__name__
        cls.entities[cls.__name__] = cls

    def register_inverse (cls, field_name, field_type, **kwargs):
        for name, field in cls._fields.iteritems():
            # FIXME: don't access private memeber Field._field
            if isinstance(field._field, field_type):
                if field._field._entity == None:
                    raise EnvironmentError("Waiting for '%s' to be defined" % name)
                elif field._field._entity == kwargs['entity']:
                    return name

        if field_name in cls._fields:
            raise NameError("%s already has a field '%s' and it's not %s" %
                            (cls.entity_name, field_name, field_type.__name__))

        setattr(cls, field_name, Field(field_type, **kwargs))
        cls._register_field(field_name, getattr(cls, field_name))

        getattr(cls, field_name).bind_to_inverse(kwargs['inverse'])

        return field_name

    def get_entity_type_by_name (cls, name):
        return cls.entities[name]

    def get_entity_from_dictionary (cls, obj):
        entity = cls.get_entity_type_by_name(obj.name)
        instance = entity(check_on_create=False, **dict(obj))

        Session.default.modify(instance, changed=False)

        return instance

    @property
    def query (cls):
        return Query(cls)

    def get (cls, pk):
        return cls.query.get(pk)

    def get_by (cls, *filters):
        return cls.query.filter_by(*filters).one()

    @property
    def meta (cls):
        class EntityMetaData (object):

            @property
            def name (metaself):
                return cls._entity_name

            @property
            def pk (metaself):
                return cls._fields[cls._pk_name]

            @property
            def singleton (metaself):
                return metaself.pk.is_singleton

        return EntityMetaData()

    @property
    def entity_pk (cls):
        return cls._fields[cls.meta.pk.name]

    @property
    def entity_has_foreign_key (cls):
        return cls.entity_pk.is_foreign_key

    @property
    def entity_foreign_key_entity (cls):
        return cls.entity_pk.foreign_key_entity

class Entity (object):

    __metaclass__ = EntityMeta

    def __new__ (cls, **fields):
        cls._constraint_fields()
        return super(Entity, cls).__new__(cls)

    def __init__ (self, **fields):
        check = fields.pop('check_on_create', True)

        self._fields = dict((k, v.field) for k, v in
                            type(self)._fields.iteritems())

        if self.meta.pk.name in fields:
            pk = fields.get(self.meta.pk.name)
            if isinstance(pk, BaseObject):
                self._fields[self.meta.pk.name].set_data(
                        self.meta.pk.unmarshal(pk), check=check)
            else:
                self._fields[self.meta.pk.name].set_data(pk, check=check)
        elif self.meta.pk.is_autoincrementing and \
           hasattr(self.entity_pk, 'set_next'):
            self.entity_pk.set_next(type(self))

        for key, val in fields.iteritems():
            if isinstance(val, BaseObject):
                self._fields[key].set_data(
                            self._fields[key].unmarshal(val), check=check,
                            instance=self)
            else:
                self._fields[key].set_data(val, check=check, instance=self)

        for key, field in type(self)._fields.iteritems():
            if key not in fields:
                if field.default == None:
                    if check:
                        self._fields[key].validate_data(instance=self)
                else:
                    self._fields[key].set_data(field.default, check=check,
                                               instance=self)

        Session.default.add(self, changed=True)

    def __eq__ (self, other):
        if not isinstance(other, Entity):
            return False

        if self.meta.name != other.meta.name:
            return False

        return self.pk == other.pk

    def __ne__ (self, other):
        return not self.__eq__(other)

    @property
    def meta (self):
        class InstanceEntityMetaData (type(type(self).meta)):

            def touch (metaself):
                Session.default.modify(self, changed=True)

        return InstanceEntityMetaData()

    @property
    def entity_pk (self):
        return self._fields[self.meta.pk.name]

    @property
    def entity_pk_value (self):
        if self.entity_has_foreign_key and self.entity_pk.get_data() != None:
            return self.pk.entity_pk_value
        else:
            return self.pk

    @property
    def entity_has_foreign_key (self):
        return type(self).entity_pk.is_foreign_key

    @property
    def entity_foreign_key_entity (self):
        return type(self).entity_pk.foreign_key_entity

    @property
    def entity_as_dictionary (self):
        res = make_object(self.meta.name, {})

        for name in type(self)._field_order:
            if not type(self)._fields[name].is_virtual:
                res.append(name, make_object(name, self._fields[name].marshal()))

        return res
        

    def field_get (self, name):
        name = name == 'pk' and self.meta.pk.name or name
        return self._fields[name].get_data(instance=self)

    def field_set (self, name, value, check=True):
        self._fields[name].set_data(value, check=check, instance=self)
        self.meta.touch()


from tesql import __author__, __license__, __version__
