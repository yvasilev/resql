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

from glob import iglob
from StringIO import StringIO

import tesql

# FIXME: Make flexible
from tesql.disk.formats.plain import write_object

from base import BaseDiskStrategy

class Related (BaseDiskStrategy):

    def __init__ (self):
        self._locations = {}

        self.bind(os.path.join(os.getcwdu(), '.tesqldb'))

    def bind (self, location):
        self._locations[None] = location

    def _bind_entity_helper (self, key, location):
        if location and location[0] == '/':
            self._locations[key] = location
        else:
            self._locations[key] = os.path.join(self.base_location, location)

    def bind_entity (self, entity, location):
        if isinstance(location, basestring):
            self._bind_entity_helper(entity.entity_name, location)
        else:
            for k, v in location.iteritems():
                if k == None:
                    key = entity.entity_name
                else:
                    key = (entity.entity_name, k)
                self._bind_entity_helper(key, v)

    def unbind_entity (self, entity):
        if entity.entity_name in self._locations:
            del self._locations[entity.entity_name]

    @property
    def base_location (self):
        return self._locations[None]

    def get_location (self, entity, pk=None):
        if entity.entity_has_foreign_key:
            if isinstance(entity, tesql.orm.Entity):
                pk = entity.entity_pk_value
            entity = entity.entity_foreign_key_entity
            return self.get_location(entity, pk)

        if isinstance(entity, tesql.orm.Entity):
            pk = entity.entity_pk_value

        if (entity.entity_name, pk) in self._locations:
            location = self._locations[entity.entity_name, pk]
        else:
            if entity.entity_name in self._locations:
                location = self._locations[entity.entity_name]
            else:
                location = os.path.join(self.base_location, entity.entity_name)

            if entity.entity_is_singleton:
                location = location + '.conf'
            else:
                if pk != None:
                    location = os.path.join(location, unicode(pk) + '.conf')

        return location

    def make_location (self, entity, pk=None):
        location = self.get_location(entity, pk)

        if isinstance(entity, type) and pk == None:
            if not os.path.exists(location):
                os.makedirs(location)
        else:
            if not os.path.exists(os.path.dirname(location)):
                os.makedirs(os.path.dirname(location))

        return location

    def list_location (self, entity, pk=None):
        location = self.get_location(entity, pk)

        if isinstance(entity, type) and pk == None:
            res = iglob(os.path.join(location, '*.conf'))

            if res and entity.entity_has_foreign_key:
                nres = []
                for path in res:
                    dicts = self.load_location_as_dictionaries(path)
                    # FIXME: add dicts to session
                    if any(x.name == entity.entity_name for x in dicts):
                        nres.append(path)

                res = nres
        else:
            res = os.path.isfile(location) and location or None

            if res and entity.entity_has_foreign_key:
                dicts = self.load_location_as_dictionaries(location)
                # FIXME: add dicts to session
                res = any(x.name == entity.entity_name for x in dicts) and \
                    res or None

        return res

    def list_primary_key (self, entity, location):
        base = entity.entity_name in self._locations and \
               self._locations[entity.entity_name] or self.base_location

        if not location.startswith(base):
            raise ValueError("Location '%s' is not reversible." % location)

        head, tail = os.path.split(location)
        return entity.entity_pk.unmarshal(tail[:-5])

    def store_location (self, instance):
        if instance.entity_has_foreign_key:
            pk = instance.entity_pk_value
            entity = instance.entity_foreign_key_entity
            instance = tesql.orm.Session.default.get(entity, pk)
            return self.store_location(instance)

        location = self.make_location(instance)

        fileobj = open(location, 'w')

        write_object(instance.entity_as_dictionary, fileobj)
        tesql.orm.Session.default.modify(instance, changed=False)

        for entity in tesql.orm.Entity.entities.itervalues():
            if entity.entity_foreign_key_entity == type(instance):
                if tesql.orm.Session.default.has(entity, instance.entity_pk_value):
                    inst = tesql.orm.Session.default.get(entity,
                                                         instance.entity_pk_value)

                    write_object(inst.entity_as_dictionary, fileobj)
                    tesql.orm.Session.default.modify(inst, changed=False)
        fileobj.close()


from tesql import __author__, __license__, __version__
