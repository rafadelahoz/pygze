# Singleton Class

class Singleton(object):
    __single = None # the one, true Singleton

    def __new__(cls, *args, **kwargs):
        if cls != type(cls.__single):
            cls.__single = object.__new__(cls, *args, **kwargs)
        return cls.__single
