"""
Metaclasses for use in the project
"""


class SingletonMeta(type):
    """
    A simple Singleton metaclass

    Copypasted from
    https://refactoring.guru/design-patterns/singleton/python/example#example-0
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Overrides a call to `MyClass()` instead of `__init__` or `__new__`
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
