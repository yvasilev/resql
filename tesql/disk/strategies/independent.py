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


class Independent (BaseDiskStrategy):

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
            self._bind_entity_helper(entity.meta.name, location)
        else:
            for k, v in location.iteritems():
                if k == None:
                    key = entity.meta.name
                else:
                    key = (entity.meta.name, k)
                self._bind_entity_helper(key, v)

    def unbind_entity (self, entity):
        if entity.meta.name in self._locations:
            del self._locations[entity.meta.name]

    @property
    def base_location (self):
        return self._locations[None]

    def get_location (self, entity, pk=None):
        if isinstance(entity, tesql.orm.Entity):
            pk = entity.pk

        if (entity.meta.name, pk) in self._locations:
            location = self._locations[entity.meta.name, pk]
        else:
            if entity.meta.name in self._locations:
                location = self._locations[entity.meta.name]
            else:
                location = os.path.join(self.base_location, entity.meta.name)

            if entity.meta.singleton:
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
            return iglob(os.path.join(location, '*.conf'))
        else:
            return os.path.isfile(location) and location or None

    def list_primary_key (self, entity, location):
        base = entity.meta.name in self._locations and \
               self._locations[entity.meta.name] or self.base_location

        if not location.startswith(base):
            raise ValueError("Location '%s' is not reversible." % location)

        head, tail = os.path.split(location)
        return entity.entity_pk.unmarshal(tail[:-5])

    def store_location (self, instance):
        location = self.make_location(instance)

        fileobj = open(location, 'w')
        write_object(instance.entity_as_dictionary, fileobj)
        fileobj.close()


from tesql import __author__, __license__, __version__
