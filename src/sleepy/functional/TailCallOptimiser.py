import inspect, sleepy, time

class __tail_call_optimised:

    def __init__ (self, fn, debug):
        self._fn = fn
        self._depth = 0
        self._count = 0
        self._args1 = None
        self._debug = (lambda x: debug.write (x + '\n')) if type (debug) is file else \
                      debug
        pass

    def __debug (self, fn):
        if self._debug is not None:
            self._debug (fn ())
            pass
        pass

    def __call__ (self, *args, **kwargs):
        self._count += 1

        self.__debug (lambda : '%s [call] __call__[n=%d,dep=%d,stack=%d] (%s, %s)' % (self._fn.__name__,
                                                                                      self._count,
                                                                                      self._depth,
                                                                                      len (inspect.stack ()),
                                                                                      args,
                                                                                      kwargs))

        if self._depth == 0:
            try:
                self._depth += 1
                args0 = (args, kwargs)

                exprs = []
                while True:
                    ret = self._fn (*args0[0], **args0[1])

                    if isinstance (ret, sleepy.functional.SimpleLambda) and (ret._this is self):
                        exprs.insert (0, ret)
                        args0 = self._args1
                    else:
                        self.__debug (lambda : '%s [last] evaluated %s with x = %s.' % (self._fn.__name__, exprs, ret))

                        y = ret
                        for expr in exprs:
                            y = expr (y)
                            pass

                        self.__debug (lambda : '%s [last] yielded %s.' % (self._fn.__name__, y))
                        return y
                    pass
                pass
            finally:
                self._depth = 0
                self._count = 0
                self._args1 = None
                pass
            pass
        else:
            self._args1 = (args, kwargs)
            lmd = sleepy.functional.SimpleLambda ()
            lmd._this = self

            return lmd
        pass

    pass

def tail_call_optimised (debug = None):
    return lambda fn: __tail_call_optimised (fn, debug)
    
tail_call_optimized = tail_call_optimised
tail_call = tail_call_optimised

if __name__ == '__main__':
    import sys

    @tail_call_optimised (debug = sys.stdout)
    def factorial (n):
        return 1                     if n == 1 else \
               n * factorial (n - 1)

    print '===== factorial(5) ====='
    print 'factorial(5) = %d' % factorial (5)
    print '\n'


    @tail_call_optimised (debug = sys.stdout)
    def even (n):
        return True        if n == 0 else \
               odd (n - 1)

    @tail_call_optimised (debug = sys.stdout)
    def odd (n):
        return False        if n == 0 else \
               even (n - 1)

    print '===== even(10) ====='
    print 'even(10) = %s' % even (10)
    print '\n'

    print '===== odd(10) ====='
    print 'odd(10) = %s' % odd (10)
    print '\n'

    pass
