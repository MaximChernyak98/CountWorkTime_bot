class Debugger(object):
    """ Debug a method and return it back"""

    enabled = False

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        if self.enabled:
            return 1
        else:
            return self.func(*args, **kwargs)
