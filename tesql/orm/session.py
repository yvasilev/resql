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

from tesql.disk.strategies import Independent
from tesql.query import Query

class CachedInstance (object):

    def __init__ (self, entity, changed=False):
        self.entity = entity
        self.changed = changed


class SessionCache (dict):

    @staticmethod
    def etokey (entity, pk=None):
        if isinstance(entity, type):
            return (entity.meta.name, pk)
        else:
            return (entity.meta.name, entity.entity_pk_value)

    def append (self, entity, changed=False):
        self[self.etokey(entity)] = CachedInstance(entity, changed)

    def remove (self, entity):
        del self[self.etokey(entity)]

    def contains (self, entity):
        return self.etokey(entity) in self

    def changed (self, entity):
        return self[self.etokey(entity)].changed


class SessionStack (object):

    def __init__ (self):
        self._stack = []

    def __contains__ (self, key):
        for level in reversed(self._stack):
            if key in level:
                return True

        return False

    def get (self, key):
        for level in reversed(self._stack):
            if key in level:
                return level[key]

        raise KeyError(key)

    @property
    def depth (self):
        return len(self._stack)

    def peek (self):
        return self._stack[-1]

    def push (self):
        if not self._stack or self.peek():
            self._stack.append(SessionCache())

    def pop (self):
        if self._stack:
            if self.peek():
                raise RuntimeError("Trying to pop a non empty stack level")
            self._stack.pop(-1)

    def contains (self, entity):
        for level in reversed(self._stack):
            if level.contains(entity):
                return True

        return False

    def append (self, instance):
        self.peek().append(instance, changed=True)

    def remove (self, instance):
        for level in reversed(self._stack):
            if level.contains(instance):
                level.remove(instance)

class SessionMeta (type):

    def __init__ (cls, name, bases, ns):
        cls._default_session = None

    def make_default (cls, session):
        cls._default_session = session

    @property
    def default (cls):
        if not cls._default_session:
            Session().be_default()

        return cls._default_session

class Session (object):

    __metaclass__ = SessionMeta

    def __init__ (self, strategy=Independent):
        """Construct a new Session."""
        self._cache = SessionCache()
        self._stack = SessionStack()
        self._strategy = strategy()

        self.begin()

    def be_default (self):
        type(self).make_default(self)

    def bind (self, location):
        self._strategy.bind(location)

    def bind_entity (self, entity, location):
        self._strategy.bind_entity(entity, location)

    def add (self, instance, changed=False):
        """Place an object in the Session."""
        if changed:
            self._stack.append(instance)

        self._cache.append(instance)

    def modify (self, instance, changed=True):
        if changed and not self._stack.contains(instance):
            location = self._strategy.get_location(instance)
            self._stack.append(instance, location)
        elif not changed and self._stack.contains(instance):
            self._stack.remove(instance)

    def has (self, entity, pk):
        key = SessionCache.etokey(entity, pk)

        if key in self._cache:
            return True

        if self._strategy.list_location(entity, pk):
            return True

        return False

    def get (self, entity, pk):
        key = SessionCache.etokey(entity, pk)
        if key in self._stack:
            return self._stack.get(key).entity

        if key not in self._cache:
            self.load(entity, pk)

        return self._cache.get(key).entity

    def list_primary_keys (self, entity):
        res = []
        for location in self._strategy.list_location(entity):
            res.append(self._strategy.list_primary_key(entity, location))

        for pk in (pk for e, pk in self._cache if e == entity.meta.name):
            if pk not in res:
                res.append(pk)

        return res

    def load (self, entity, pk):
        self._strategy.load_location(entity, pk)

    def store (self, instance):
        self._strategy.store_location(instance)

        if self._stack.contains(instance):
            self._stack.remove(instance)

    def begin (self):
        """Begin a transaction on this Session."""
        self._stack.push()

    def close (self):
        """Close this Session."""
        self._stack.pop()

    def commit (self):
        """Flush pending changes and commit the current transaction."""
        self.flush()

        self._stack.pop()
        if self._stack.depth == 0:
            self.begin()

    def delete (self, instance):
        """Mark an instance as deleted."""
        pass

    def expunge (self, instance=None):
        """Remove the instance from this Session."""
        if instance:
            if self._stack.contains(instance):
                self._stack.remove(instance)
            if self._cache.contains(instance):
                self._cache.remove(instance)
        else:
            while self._stack.depth >= 1:
                for key in self._stack.peek().keys():
                    del self._stack.peek()[key]
                self._stack.pop()

            for key in self._cache.keys():
                del self._cache[key]

            self.begin()

    def flush (self):
        """Flush all the object changes to the database."""
        for instance in self._stack.peek().values():
            self.store(instance.entity)

    def query (self, *args, **kw):
        """Return a new Query object corresponding to this Session."""
        pass

    def refresh (self, instance):
        """Refresh the attributes on the given instance."""
        pass

    def rollback (self):
        """Rollback the current transaction in progress."""
        pass


from tesql import __author__, __license__, __version__
