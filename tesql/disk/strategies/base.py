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
from StringIO import StringIO

import tesql

# FIXME: Make flexible
from tesql.disk.formats.plain import read_object


class BaseDiskStrategy (object):

    def load_location_as_dictionaries (self, location):
        if not os.path.isfile(location):
            raise IOError("File '%s' not found" % location)

        # FIXME: Check why it does not work directly on fileobj
        fileobj = open(location, 'rU')
        striofile = StringIO(fileobj.read())
        fileobj.close()

        res = []
        obj = read_object(striofile)
        while obj:
            res.append(obj)
            obj = read_object(striofile)

        return res

    def load_location (self, entity, pk):
        location = self.get_location(entity, pk)

        dicts = self.load_location_as_dictionaries(location)

        res = []
        for obj in dicts:
            objentity = tesql.orm.Entity.get_entity_type_by_name(obj.name)
            if objentity.meta.pk.name not in obj:
                obj[objentity.meta.pk.name] = str(pk)

            res.append(tesql.orm.Entity.get_entity_from_dictionary(obj))

        if len(res) == 1:
            return res[0]
        else:
            return res


from tesql import __author__, __license__, __version__
