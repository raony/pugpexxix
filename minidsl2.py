# Mini DSL

class Validated(object):
    rules = {}

    def __validate__(self, key, value):
        for msg, rule in self.rules.get(key, {}).items():
            if not rule(value):
                raise ValueError('%s: %s'%(key, msg))

    def __init__(self, values_dict):
        for key, value in values_dict.items():
            self.__validate__(key, value)
            setattr(self, key, value)

    def __setattr__(self, key, value):
        self.__validate__(key, value)
        super(Validated, self).__setattr__(key, value)


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

    def __init__(self, username, email):
        super(User, self).__init__({'username': username, 'email': email})

class Account(Validated):
    rules = {
        'number': {
            'deve ser maior que 0': lambda value: value > 0,
            'deve ser menor que 999': lambda value: value < 999,
        },
    }

    def __init__(self, number, bank):
        super(Account, self).__init__({'number': number, 'bank': bank})
