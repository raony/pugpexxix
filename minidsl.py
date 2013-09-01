# Mini DSL

# the purpose of this module is to provide some way of easily
# define structures with validations rules.

# one way of using it is:

# >>> import minidsl
# >>> class Profile(minidsl.Validated):
# ...     rules = {
# ...         'age': {
# ...             'should be greater than 18.': lambda age: age >= 18,
# ...             'should be lesser than 78.': lambda age: age < 78,
# ...         },
# ...         'color': {
# ...             'should be a valid color.': lambda color: color in ('blue', 'red', 'yellow'),
# ...         },
# ...     }
# ...
# >>> assert Profile(18, 'red') # was created correctly
# >>> try:
# ...     Profile(14, 'red')
# ...     assert False # exception was raised
# ... except ValueError, e, msg:
# ...     assert msg == 'age: should be greater than 18.'

# mini dsls are indeed useful, you can see a lot of it in Django and other frameworks! Are you creating
# a framework? No? Then why do you think it's gonna be useful for you?

# things that are easy to use may not be easy to maintain. Mind this trade off.

class ValidatedAttr(object):
    # this is the descriptor that take the rules and run it at __set__ calls
    def __init__(self, name, rules = {}):
        self.rules = rules
        self.name = name

    @property
    def iname(self):
        # unfortunately python 2 still don't have the nice descriptor definition of python 3 and
        # we need to store the real value in an internal attribute
        return '_%s'%self.name

    def __get__(self, instance, cls):
        return getattr(instance, self.iname, None)

    def __set__(self, instance, value):
        # validate the rules and save the value
        for msg, rule in self.rules.items():
            if not rule(value):
                raise ValueError('%s: %s'%(self.name, msg))
        setattr(instance, self.iname, value)

class ValidatedMeta(type):
    # we need a metaclass because we're going to populate the descriptors in the class based
    # on its "rules" dict.

    # aaand I would like to make a useful __init__ statement as well.

    def __new__(cls, name, bases, clsdict):
        # here I build the nice signature of __init__ for the class, so the user can have
        # more context when introspecting the class.
        keys = clsdict.get('rules', {}).keys()
        code = 'def __init__(%s):\n'%', '.join(['self'] + keys)
        if keys:
            code += '\n'.join(['    self.%s = %s'%(key, key) for key in keys])
        else:
            code += '    pass'
        exec code in clsdict
        return type.__new__(cls, name, bases, clsdict)


    def __init__(self, name, bases, clsdict):
        # populate the descriptors
        for key, rules in clsdict.get('rules', {}).items():
            setattr(self, key, ValidatedAttr(key, rules))


class Validated(object):
    # the base class with the metaclass
    __metaclass__ = ValidatedMeta
    rules = {}

import re
EMAIL_REGEX = re.compile(r'[^@]+@[^@]+\.[^@]+')

class User(Validated):
    rules = {
        'email': {
            'deve ser um email valido': lambda value: EMAIL_REGEX.match(value),
        },
        'username': {
            'deve conter ate 8 caracteres': lambda value: len(value) <= 8,
        },
    }

class Account(Validated):
    rules = {
        'number': {
            'deve ser maior que 0': lambda value: value > 0,
            'deve ser menor que 999': lambda value: value < 999,
        },
        'bank': {
        },
    }

