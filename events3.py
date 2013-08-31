# Event dispatcher

event_callbacks  = {}

def register(event, callback):
    event_callbacks.setdefault(event, []).append(callback)

def fire(event):
    for callback in event_callbacks.get(event, []):
        callback()

class Listener(object):
    def __init__(self, *args, **kwargs):
        super(Listener, self).__init__(*args, **kwargs)
        for attr in dir(self):
            attr = getattr(self, attr)
            if callable(attr) and hasattr(attr, 'listen_to'):
                register(attr.listen_to, attr)

def listen_to(event):
    def decorator(f):
        f.listen_to = event
        return f
    return decorator
