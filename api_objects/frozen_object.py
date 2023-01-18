from abc import ABC, abstractmethod

from general_utils.mongo_general_utils import remove_mongo_id


class FrozenObject(ABC, object):
    __is_frozen = False

    @abstractmethod
    def __init__(self, *args, **kwargs):
        raise NotImplementedError()

    def __setattr__(self, key, value):
        if self.__is_frozen and not hasattr(self, key):
            raise TypeError("%r is a frozen class" % self)
        object.__setattr__(self, key, value)

    def __new__(cls, *args, **kwargs):
        instance = object.__new__(cls)
        instance.__init__(*args, **kwargs)
        instance.__is_frozen = True
        return instance

    def _freeze(self):
        self.__is_frozen = True

    def convert_to_dict(self):
        return {
            k: v for k, v in vars(self).items() if '__is_frozen' not in k
        }

    @classmethod
    def from_dict(cls, data: dict):
        remove_mongo_id(data=data)
        return cls.__new__(cls, **data)
