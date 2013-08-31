# Event dispatcher

# this example aims to illustrate how the desire for syntact sugar can
# lead to abuse of metaprogramming.

# how this module is supposed to work:
# >>> import events

# >>> @events.listener
# ... class MyListener(object):

# ...     def light_on(self):
# ...         print "light's on!"

# ...     def knock(self):
# ...         print "who's there?"
# ...
# >>> events.light_on() # firing the event, but no one's listening
# >>> obj = MyListener() # now someone registers
# >>> events.light_on()
# light's on!
# >>> events.knock()
# who's there?
# >>> events.light_off()
# >>>

# one can see that you just need to decorate the class and use
# a name convention for the methods, so they can act as callbacks for
# the events.

# and if we need to add a new callback dynamically?

# >>> from types import MethodType
# >>> def light_off(self):
# ...     print 'you will die of old age before needing to use MethodType!'
# >>> obj.light_off = MethodType(new_callback, obj)

# >>> events.light_off() # now you just need to fire the event!
# you will die of old age before needing to use MethodType!

# HINT 1: Do not enforce magic by convention. Do not try to create 
# syntactic sugar, you are not a language architect, you are a programmer. 
# You use languages, not create them.

# this is the possible events, it is kind of useless because after
# loading the module, they're going to be hardcoded on it, and changing 
# this list will not any effect afterwards.
_events = [
    'light_on',
    'light_off',
    'knock',
]

_listeners = []

def listener(klass):
    # receives class to be decorated, we're going to swap __init__
    # for a version where it registers itself as a listener
    # remember: self here is an *instance* of the decorated class
    def __init__(self, *args, **kwargs):
        super(klass, self).__init__(*args, **kwargs)
        _listeners.append(self)
    klass.__init__ = __init__
    return klass


def __init():
    class _eventcls(object):
        # callable that will fire the event
        # i.e., events.light_on()
        def __init__(self, name):
            self.name = name
        def __call__(self):
            for listener in _listeners:
                if hasattr(listener, self.name):
                    getattr(listener, self.name)()
    current_module = __import__(__name__)
    for event in _events:
        # we hardcode the callables to the current module in order
        # to be accessed as intended
        setattr(current_module, event, _eventcls(event))

__init()
del __init
#  do things inside a func and cleanup locals, so module will be clean
