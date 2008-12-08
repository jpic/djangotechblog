
from threading import RLock

class RejectBroadcast(Exception):
    pass

class _Reciever(object):

    def __init__(self, name, callable, priority):
        self.name = name
        self.callable = callable
        self.priority = priority

    def __call__(self, *args, **kwargs):
        return self.callable(*args, **kwargs)

    def __cmp__(self, other):
        return cmp(self.priority, other.priority)


class Broadcaster(object):

    def __init__(self):
        self._lock = RLock()
        self.recievers_map = {}


    def _get_recievers(self, func_name):
        self._lock.acquire()
        try:
            return self.recievers_map.get(func_name, [])[:]
        finally:
            self._lock.release()


    def register(self, func_name, callable, priority=100):

        self._lock.acquire()
        try:
            reciever = _Reciever(func_name, callable, priority)

            recievers = self.recievers_map.setdefault(func_name, [])
            recievers.append(reciever)
            recievers.sort(reverse=True)
        finally:
            self._lock.release()


    def call(self, func_name, *args, **kwargs):

        """Return the result of the highest priority callable that doesn't reject the broadcast."""

        recievers = self._get_recievers(func_name)
        for reciever in recievers:
            try:
                return reciever(*args, **kwargs)
            except RejectBroadcast:
                continue
        return None


    def first(self, func_name, *args, **kwargs):

        """Return the first result that doesn't evaluate to False."""

        recievers = self._get_recievers(func_name)
        for reciever in recievers:
            try:
                result = reciever(*args, **kwargs)
                if result:
                    return result
            except RejectBroadcast:
                continue
        return None


    def call_all(self, func_name, *args, **kwargs):

        """Calls all the callables that don't return the broadcast, and
        returns a list of the return values."""

        recievers = self._get_recievers(func_name)
        results = []
        for reciever in recievers:
            try:
                result = reciever(*args, **kwargs)
            except RejectBroadcast:
                continue
            results.append(result)
        return results


    def __contains__(self, func_name):
        self._lock.acquire()
        try:
            return func_name in self.recievers_map
        finally:
            self._lock.release()


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

        @reciever()
        def printer3(what):
            print what, "3"
            return 3

        print call.go("Hello!")
        print all.go("Hello!")
        print all.notexist("Hello!")
        call.printer3("test")

    main()