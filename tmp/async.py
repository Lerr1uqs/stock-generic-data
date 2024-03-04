from typing import Callable
from functools import wraps

def check_data_loaded(f: Callable) -> Callable:

    @wraps(f)
    def wrapper(self, *args, **kwargs):
        t = type(self)
        if t.loaded is False:
            raise RuntimeError
        ret = f(self, *args, **kwargs)
        return ret

    return wrapper

class A:
    loaded = False

    @check_data_loaded
    def a(self):
        return 1


a = A()
A.loaded = True
print(a.a())