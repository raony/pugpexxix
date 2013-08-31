# Event dispatcher

_events = [
    'light_on',
    'light_off',
    'knock',
]

_listeners = []

def listener(klass):
    def __init__(self, *args, **kwargs):
        super(klass, self).__init__(*args, **kwargs)
        _listeners.append(self)
    klass.__init__ = __init__
    return klass


def __init():
    class _eventcls(object):
        def __init__(self, name):
            self.name = name
        def __call__(self):
            for listener in _listeners:
                if hasattr(listener, self.name):
                    getattr(listener, self.name)()
    current_module = __import__(__name__)
    for event in _events:
        setattr(current_module, event, _eventcls(event))

__init()
del __init
