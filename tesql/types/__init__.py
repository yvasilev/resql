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

from numeric import Indexer
from numeric import Integer
from text import String

from references import OneToOne
from references import OneToMany
from references import ManyToOne
from references import ManyToMany

from references import QueryOneToOne
from references import QueryOneToMany
from references import QueryManyToOne
from references import QueryManyToMany

__all__ = ['Indexer', 'Integer', 'String',
           'OneToOne', 'OneToMany', 'ManyToOne', 'ManyToMany',
           'QueryOneToOne', 'QueryOneToMany', 'QueryManyToOne', 'QueryManyToMany']


from tesql import __author__, __license__, __version__
