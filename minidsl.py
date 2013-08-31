# Mini DSL

class ValidatedAttr(object):
    def __init__(self, name, rules = {}):
        self.rules = rules
        self.name = name

    @property
    def iname(self):
        return '_%s'%self.name

    def __get__(self, instance, cls):
        return getattr(instance, self.iname, None)

    def __set__(self, instance, value):
        for msg, rule in self.rules.items():
            if not rule(value):
                raise ValueError('%s: %s'%(self.name, msg))
        setattr(instance, self.iname, value)

class ValidatedMeta(type):

    def __new__(cls, name, bases, clsdict):
        keys = clsdict.get('rules', {}).keys()
        code = 'def __init__(%s):\n'%', '.join(['self'] + keys)
        if keys:
            code += '\n'.join(['    self.%s = %s'%(key, key) for key in keys])
        else:
            code += '    pass'
        exec code in clsdict
        return type.__new__(cls, name, bases, clsdict)


    def __init__(self, name, bases, clsdict):
        for key, rules in clsdict.get('rules', {}).items():
            setattr(self, key, ValidatedAttr(key, rules))


class Validated(object):
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

