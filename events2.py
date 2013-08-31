# Event dispatcher

class eventmod(object):
    class _eventcls(object):
        def __init__(self, name, listeners):
            self.name = name
            self.listeners = listeners
        def __call__(self):
            for listener in self.listeners:
                if hasattr(listener, self.name):
                    getattr(listener, self.name)()

    _listeners = []

    @classmethod
    def listener(cls, klass):
        def __init__(self, *args, **kwargs):
            super(klass, self).__init__(*args, **kwargs)
            cls._listeners.append(self)
        klass.__init__ = __init__
        return klass


    def __getattr__(self, value):
        return self._eventcls(value, self._listeners)

import sys
sys.modules[__name__] = eventmod()

