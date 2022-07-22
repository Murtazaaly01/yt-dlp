# coding: utf-8
import re

from ..utils import bug_reports_message, write_string


class LazyLoadMetaClass(type):
    def __getattr__(self, name):
        if '_real_class' not in self.__dict__:
            write_string(
                f'WARNING: Falling back to normal extractor since lazy extractor {self.__name__} does not have attribute {name}{bug_reports_message()}'
            )

        return getattr(self._get_real_class(), name)


class LazyLoadExtractor(metaclass=LazyLoadMetaClass):
    _module = None
    _WORKING = True

    @classmethod
    def _get_real_class(cls):
        if '_real_class' not in cls.__dict__:
            mod = __import__(cls._module, fromlist=(cls.__name__,))
            cls._real_class = getattr(mod, cls.__name__)
        return cls._real_class

    def __new__(cls, *args, **kwargs):
        real_cls = cls._get_real_class()
        instance = real_cls.__new__(real_cls)
        instance.__init__(*args, **kwargs)
        return instance
