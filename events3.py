# Event dispatcher

# this is a better way of how I think an event dispatcher should be.

# this use an explicit dictionary for (event, callbacks)
# we have sound methods for registering listeners and firing events
# we use some decoration and mixins to add syntactic sugar, but just a bit

# how it may works:

# >>> import events3

# >>> class MyListener(events3.Listener):
# ...     @listen_to('light_on')
# ...     def warn(self): # method names no longer need to equal event name
# ...         print "light's on!"
# ...     @listen_to('knock')
# ...     def ask(self):
# ...         print "who's there?"

# >>> obj = MyListener()
# >>> events3.fire('light_on')
# light's on!
# >>> events3.fire('knock')
# who's there?

# now it is clear which method is hooked to which event.
# there is no difference in using strings as event names, one may
# say that it is DRY violation, but seriously, repeating a method call
# is not anyway better. We do not have compilation check, the error would
# sprout in the same moment at runtime.
# and if we need to hook a callback on the fly?

# >>> from types import MethodType
# >>> def new_callback(self):
# ...     print 'you will die of old age before needing to use MethodType!'
# >>> obj.new_callback = MethodType(new_callback, obj)
# >>> events3.register('shutdown', obj.new_callback) 

# the listen_decorator has no use here, as the object was already 
# initialized.

# >>> events3.fire('shutdown')
# you will die of old age before needing to use MethodType!

event_callbacks  = {}

def register(event, callback):
    event_callbacks.setdefault(event, []).append(callback)

def fire(event):
    for callback in event_callbacks.get(event, []):
        callback()

class Listener(object):
    def __init__(self, *args, **kwargs):
        # this mixin tries not to disrupt the mro chain for calling super
        super(Listener, self).__init__(*args, **kwargs)
        for attr in dir(self):
            attr = getattr(self, attr)
            if callable(attr) and hasattr(attr, 'listen_to'):
                # it uses an method attribute to decide if the method
                # is a callback and who it listens to
                register(attr.listen_to, attr)

def listen_to(event):
    # decorator with parameter, first receives the parameter and
    # then returns the decorator
    def decorator(f):
        # the decorator needs only to add the listen_to property
        # to the callable. This way, encapsulating logic in this module
        f.listen_to = event
        return f
    return decorator
