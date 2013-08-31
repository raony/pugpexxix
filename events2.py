# Event dispatcher

# things get nastier here as we get rid of the events list and
# through a __getattr__ in the module, we now may accept any arbitrary
# call as the triggering of a event with the same name.

# things may work this way:

# >>> import events2
# >>> @events2.listener
# ... class MyListener(object):
# ...     def foo(self):
# ...         print 'bar!'
# ...
# >>> obj = MyListener() # registering to events
# >>> events2.foo() # arbitrary event
# bar!

# we don't need to say that this can be tricky as methods unrelated
# to events logic may get called if you fire an event with the same
# name. Shame on you for trying to be a pro-grammer!

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

# this is a hack in order to __getattr__ to work, and it only works
# when defined at the object class, not the object itself. Thus, we
# create a proxy class just to instantiate an object and pass it as
# the module
import sys
sys.modules[__name__] = eventmod()

