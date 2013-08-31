# Hijacking third party libs

from functools import wraps
import imp
import inspect
import sys

def logall(f):
    @wraps(f)
    def _f(*args, **kwargs):
        print '*** %s' % f.__name__
        return f(*args, **kwargs)
    return _f

class logallmeta(type):
    def __new__(cls, name, bases, clsdict):
        for attr, attrvalue in clsdict.items():
            if callable(attrvalue):
                clsdict[attr] = logall(attrvalue)
        return type.__new__(cls, name, bases, clsdict)

class baselogall(object):
    __metaclass__ = logallmeta

def insert_finder():
    sys.meta_path.append(module_finder())

class module_finder(object):
    def find_module(self, fullname, path=None):
        return module_loader(*imp.find_module(fullname, path)) 

class module_loader(object):
    def __init__(self, file, pathname, description):
        self.file = file
        self.pathname = pathname
        self.description = description


    def load_module(self, fullname):
        try:
            mod = imp.load_module(fullname, self.file, self.pathname, self.description)
        finally:
            if self.file:
                self.file.close()
        dct = {'__module__':mod.__name__}
        for key, val in mod.__dict__.items():
            if inspect.isclass(val):
                try:
                    setattr(mod, key, type(key,(val,baselogall),dct))
                except TypeError, e:
                    print e
            elif callable(val):
                setattr(mod, key, logall(val))
        return mod 

