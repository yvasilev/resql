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
import re

from tesql.disk.objects import make_object
from tesql.disk.objects import String
from tesql.disk.objects import Dictionary

from tesql.disk.formats.plain import write_object
from tesql.disk.formats.plain import read_object

from base import BasePlainObject


class StringObject (BasePlainObject):

    def __init__ (self):
        super(StringObject, self).__init__()

    @property
    def priority (self):
        return 10

    @property
    def match_type (self):
        return String

    @property
    def match_re (self):
        return re.compile(r'^([\w.-]+)([:=]) (.*)$')

    def write (self, string, fileobj, prefix=''):
        lines = string.split('\n')
        lines[0] = string.name + ': ' + lines[0]

        for i in xrange(len(lines)):
            if i and not lines[i]:
                lines[i] = '.'
            fileobj.write((i and ' ' or '') + lines[i] + '\n')

    def read (self, fileobj, match=None):
        if not match:
            line = fileobj.readline()
            match = self.match_re.match(line)
            if not match or not match.groups():
                fileobj.seek(-len(line), os.SEEK_CUR)
                raise SyntaxError("'%s'" % line)

        name = match.group(1)
        value = match.group(3)

        cont_re = re.compile(r'^ (\.|.+)$')

        for line in fileobj:
            match = cont_re.match(line)
            if match and match.groups():
                value += match.group(1) == '.' and '\n' or \
                         ('\n' + match.group(1))
            else:
                fileobj.seek(-len(line), os.SEEK_CUR)
                break

        return make_object(name, value)


class ListObject (BasePlainObject):

    def __init__ (self):
        super(ListObject, self).__init__()

    @property
    def priority (self):
        return 1

    @property
    def match_type (self):
        return List

    @property
    def match_re (self):
        # FIXME: Deside how to store. like:?
        # lala = a, b, c
        # lala = a
        # lala =
        return re.compile(r'^([\w.-]+)([:=]) (([])+)$')


class DictionaryObject (BasePlainObject):

    def __init__ (self):
        super(DictionaryObject, self).__init__()

    @property
    def priority (self):
        return 100

    @property
    def match_type (self):
        return Dictionary

    @property
    def match_re (self):
        return re.compile(r'^\[([\w.-]+)\]$')

    def write (self, dictionary, fileobj, prefix=''):
        if dictionary.name:
            fileobj.write('\n[%s]\n' % (prefix + dictionary.name))

        fileobj.write('\n')

        for obj in dictionary.itervalues():
            write_object(obj, fileobj, prefix=(prefix + dictionary.name + '.'))

    def read (self, fileobj, match=None):
        if not match:
            for line in fileobj:
                if line.strip():
                    match = self.match_re.match(line)
                    if not match or not match.groups():
                        fileobj.seek(-len(line), os.SEEK_CUR)
                    break

        name = match and match.group(1) or ''
        obj = make_object(name, {})

        for line in fileobj:
            if not line.strip():
                continue

            match = self.match_re.match(line)
            if match and match.groups():
                if match.group(1)[:len(name)] != name or \
                   len(name) >= len(match.group(1)):
                    # A section, but not a sub-section
                    fileobj.seek(-len(line), os.SEEK_CUR)
                    break

                obj.append(match.group(1), self.read(fileobj, match))
            else:
                fileobj.seek(-len(line), os.SEEK_CUR)
                tobj = read_object(fileobj)
                obj.append(tobj.name, tobj)

        return obj


from tesql import __author__, __license__, __version__
