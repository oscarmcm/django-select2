import copy
import warnings
from collections import OrderedDict

from django.utils import six
# from django.utils.deprecation import RemovedInDjango19Warning

"""
Simple copy from django.utils.datastructures
this class was deprecated in django >1.9
"""
class MergeDict(object):
    """
    A simple class for creating new "virtual" dictionaries that actually look
    up values in more than one dictionary, passed in the constructor.

    If a key appears in more than one of the given dictionaries, only the
    first occurrence will be used.
    """
    def __init__(self, *dicts):
        # warnings.warn('`MergeDict` is deprecated, use `dict.update()` '
        #               'instead.', RemovedInDjango19Warning, 2)
        self.dicts = dicts

    def __bool__(self):
        return any(self.dicts)

    def __nonzero__(self):
        return type(self).__bool__(self)

    def __getitem__(self, key):
        for dict_ in self.dicts:
            try:
                return dict_[key]
            except KeyError:
                pass
        raise KeyError(key)

    def __copy__(self):
        return self.__class__(*self.dicts)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    # This is used by MergeDicts of MultiValueDicts.
    def getlist(self, key):
        for dict_ in self.dicts:
            if key in dict_:
                return dict_.getlist(key)
        return []

    def _iteritems(self):
        seen = set()
        for dict_ in self.dicts:
            for item in six.iteritems(dict_):
                k = item[0]
                if k in seen:
                    continue
                seen.add(k)
                yield item

    def _iterkeys(self):
        for k, v in self._iteritems():
            yield k

    def _itervalues(self):
        for k, v in self._iteritems():
            yield v

    if six.PY3:
        items = _iteritems
        keys = _iterkeys
        values = _itervalues
    else:
        iteritems = _iteritems
        iterkeys = _iterkeys
        itervalues = _itervalues

        def items(self):
            return list(self.iteritems())

        def keys(self):
            return list(self.iterkeys())

        def values(self):
            return list(self.itervalues())

    def has_key(self, key):
        for dict_ in self.dicts:
            if key in dict_:
                return True
        return False

    __contains__ = has_key

    __iter__ = _iterkeys

    def copy(self):
        """Returns a copy of this object."""
        return self.__copy__()

    def __str__(self):
        '''
        Returns something like

            "{'key1': 'val1', 'key2': 'val2', 'key3': 'val3'}"

        instead of the generic "<object meta-data>" inherited from object.
        '''
        return str(dict(self.items()))

    def __repr__(self):
        '''
        Returns something like

            MergeDict({'key1': 'val1', 'key2': 'val2'}, {'key3': 'val3'})

        instead of generic "<object meta-data>" inherited from object.
        '''
        dictreprs = ', '.join(repr(d) for d in self.dicts)
        return '%s(%s)' % (self.__class__.__name__, dictreprs)
