# Hijacking third party libs

# now things are going to get serious.

# imagine you need to put some code inside a third party lib. Let's say
# it is some logging feature so you can understand some wacky behavior.
# you don't know where this will lead you, and you are exploring 
# alternatives to learn more about the code without having to alter it in
# some way that it's gonna to be hard to keep it up to its new versions.

# that's when black arts come into hand, it is **exploratory** and
# **temporary**, it unleashes the depths of the system innerworks in order
# to give you insight. Please, clean up after use.

# this is how it is supposed to work:

# >>> import blackart
# >>> blackart.insert_finder() # hook into sys.meta_path
# >>> import math # (almost) any lib will do
# >>> math.ceil(1.2)
# *** ceil
# 2.0

# this is actually a partial implementation of the idea, it lacks
# the ability to successfully intercept dotted imports. It will leave
# untouched classes already with __metaclass__, and also those who lives
# on C code.

# but you get the idea.


from functools import wraps
import imp
import inspect
import sys

def logall(f):
    # my simple decorator to log functions
    @wraps(f)
    def _f(*args, **kwargs):
        print '*** %s' % f.__name__
        return f(*args, **kwargs)
    return _f

class logallmeta(type):
    # my metaclass that decorates all the class methods
    def __new__(cls, name, bases, clsdict):
        for attr, attrvalue in clsdict.items():
            if callable(attrvalue):
                clsdict[attr] = logall(attrvalue)
        return type.__new__(cls, name, bases, clsdict)

class baselogall(object):
    # my base class that uses the metaclass, so is just throw it at
    # "bases" list
    __metaclass__ = logallmeta

def insert_finder():
    # hijacking the import system!
    sys.meta_path.append(module_finder())

class module_finder(object):
    # first each import will call the find_module and expect a loader
    def find_module(self, fullname, path=None):
        return module_loader(*imp.find_module(fullname, path)) 

class module_loader(object):
    def __init__(self, file, pathname, description):
        self.file = file
        self.pathname = pathname
        self.description = description


    def load_module(self, fullname):
        # then the import will try to load_module and expect the mod
        try:
            mod = imp.load_module(fullname, self.file, self.pathname, self.description)
        finally:
            if self.file:
                self.file.close()
        dct = {'__module__':mod.__name__}
        for key, val in mod.__dict__.items():
            if inspect.isclass(val):
                try:
                    # recreate all classes with the logging base class
                    setattr(mod, key, type(key,(val,baselogall),dct))
                except TypeError, e:
                    print e
            elif callable(val):
                # decorate all the callables
                setattr(mod, key, logall(val))
        return mod 

