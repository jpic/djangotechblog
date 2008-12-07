
from threading import RLock

class RejectBroadcast(Exception):
    pass

class _Reciever(object):

    def __init__(self, name, callable, priority):
        self.name = name
        self.callable = callable
        self.priority = priority

    def __call__(self, *args, **kwargs):
        if self.callable is not None:
            return self.callable(*args, **kwargs)

    def __cmp__(self, other):
        return cmp(self.priority, other.priority)


class Broadcaster(object):

    def __init__(self):
        self._lock = RLock()
        self.recievers = {}

    def register(self, func_name, callable, priority=100):

        self._lock.acquire()
        try:
            reciever = _Reciever(func_name, callable, priority)

            recievers = self.recievers.setdefault(func_name, [])
            recievers.append(reciever)
            recievers.sort(reverse=True)
        finally:
            self._lock.release()

    def call(self, func_name, *args, **kwargs):
        """Return the result of the highest priority callable that doesn't reject the broadcast."""
        self._lock.acquire()
        recievers = self.recievers.get(func_name, [])[:]
        try:
            for reciever in recievers:
                try:
                    return reciever(*args, **kwargs)
                except RejectBroadcast:
                    continue
            return None
        finally:
            self._lock.release

    def first(self, func_name, *args, **kwargs):
        """Return the first result that doesn't avaluate to False."""

        self._lock.acquire()
        recievers = self.recievers.get(func_name, [])[:]
        try:
            for reciever in recievers:
                try:
                    result = reciever(*args, **kwargs)
                    if result:
                        return result
                except RejectBroadcast:
                    continue
            return None
        finally:
            self._lock.release


    def call_all(self, func_name, *args, **kwargs):

        """Calls all the callables that don't return the broadcast, and
        returns a list of the return values."""

        self._lock.acquire()
        try:
            recievers = self.recievers.get(func_name, [])[:]
            results = []
            for reciever in recievers:
                try:
                    result = reciever(*args, **kwargs)
                except RejectBroadcast:
                    pass
                else:
                    results.append(result)
            return results
        finally:
            return results

    def __contains__(self, func_name):
        return func_name in self.recievers


class CallProxy(object):
    def __init__(self, broadcaster, callable):
        self._broadcaster = broadcaster
        self._callable = callable

    def __getattr__(self, func_name):
        def do_call(*args, **kwargs):
            return self._callable(func_name, *args, **kwargs)
        return do_call


broadcaster = Broadcaster()

call = CallProxy(broadcaster, broadcaster.call)
all = CallProxy(broadcaster, broadcaster.call_all)
first = CallProxy(broadcaster, broadcaster.first)

def reciever(func_name=None, priority=100):
    """Register a callable as a recievers."""
    def wrap(f):
        broadcaster.register(func_name or f.__name__, f, priority)
        return f
    return wrap



if __name__ == "__main__":

    def main():

        @reciever("go")
        def printer1(what):
            print what, "1"
            return 1

        @reciever("go", 50)
        def printer2(what):
            print what, "2"
            return 2

        @reciever("go")
        def printer1(what):
            print what, "3"
            return 3

        print call.go("Hello!")
        print all.go("Hello!")
        print all.notexist("Hello!")

    main()