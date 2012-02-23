import types
from AaValueError import *

conds = {}

class Redirectable: pass

class Meta (type):

    def __init__ (cls, name, bases, dict):
        if name != "Cond":
            conds[name] = cls
            pass
        pass

    pass

class Condition:

    __metaclass__ = Meta

    pass

class and_ (Condition):

    def __init__ (self, *conds):
        self._conds = list (conds)
        pass

    def validate (self, name, x):
        excs = []
        for cond in self._conds:
            try:
                cond.validate (name, x)
            except AaValueError as e:
                excs.append (e)
                break
            pass

        if len (excs) > 0:
            raise AaValueError (" and ".join (map (lambda x: "(" + x.getConditionStr () + ")", self._conds)),
                                excs[0].actual)
        pass

    def getConditionStr (self):
        return " and ".join (map (lambda x: "(" + x.getConditionStr () + ")", self._conds))

    def __repr__ (self):
        return "and(%s)" % ", ".join (map (repr, self._conds))

    pass


class cc (Condition):

    def __init__ (self, v0, v1):
        self._v0 = v0
        self._v1 = v1
        pass

    def validate (self, name, x):
        if not (self._v0 <= x <= self._v1):
            raise AaValueError ("in [%s, %s]" % (self._v0, self._v1),
                                "%s not in [%s, %s]" % (x, self._v0, self._v1))
        pass

    def getConditionStr (self):
        return "in [%s, %s]" % (self._v0, self._v1)

    def __repr__ (self):
        return "cc(%s, %s)" % (self._v0, self._v1)
    
    pass

class co (Condition):

    def __init__ (self, v0, v1):
        self._v0 = v0
        self._v1 = v1
        pass

    def validate (self, name, x):
        if not (self._v0 <= x < self._v1):
            raise AaValueError ("in [%s, %s)" % (self._v0, self._v1),
                                "%s not in [%s, %s)" % (x, self._v0, self._v1))
        pass

    def getConditionStr (self):
        return "in [%s, %s)" % (self._v0, self._v1)

    def __repr__ (self):
        return "co(%s, %s)" % (self._v0, self._v1)
    
    pass


class oc (Condition):

    def __init__ (self, v0, v1):
        self._v0 = v0
        self._v1 = v1
        pass

    def validate (self, name, x):
        if not (self._v0 < x <= self._v1):
            raise AaValueError ("in (%s, %s]" % (self._v0, self._v1),
                                "%s not in (%s, %s]" % (x, self._v0, self._v1))
        pass

    def getConditionStr (self):
        return "in (%s, %s]" % (self._v0, self._v1)

    def __repr__ (self):
        return "oc(%s, %s)" % (self._v0, self._v1)
    
    pass


class oo (Condition):

    def __init__ (self, v0, v1):
        self._v0 = v0
        self._v1 = v1
        pass

    def validate (self, name, x):
        if not (self._v0 < x < self._v1):
            raise AaValueError ("in (%s, %s)" % (self._v0, self._v1),
                                "%s not in (%s, %s)" % (x, self._v0, self._v1))
        pass

    def getConditionStr (self):
        return "in (%s, %s)" % (self._v0, self._v1)

    def __repr__ (self):
        return "oo(%s, %s)" % (self._v0, self._v1)
    
    pass

class eq (Condition):

    def __init__ (self, value):
        self._value = value
        pass

    def validate (self, name, x):
        if x != self._value:
            raise AaValueError ("== %s" % self._value,
                                "%d (!= %d)" % (x, self._value))
        pass

    def getConditionStr (self):
        return "== %s" % self._value

    def __repr__ (self):
        return "eq(%s)" % self._value

    pass


class ne (Condition):

    def __init__ (self, value):
        self._value = value
        pass

    def validate (self, name, x):
        if x == self._value:
            raise AaValueError ("!= %s" % self._value,
                                "%d (== %d)" % (x, self._value))
        pass

    def getConditionStr (self):
        return "!= %s" % self._value

    def __repr__ (self):
        return "ne(%s)" % self._value

    pass


class ge (Condition):

    def __init__ (self, value):
        self._value = value
        pass

    def validate (self, name, x):
        if x < self._value:
            raise AaValueError (">= %s" % self._value,
                                "%d (< %d)" % (x, self._value))
        pass

    def getConditionStr (self):
        return ">= %s" % self._value

    def __repr__ (self):
        return "ge(%s)" % self._value

    pass

class gt (Condition):

    def __init__ (self, value):
        self._value = value
        pass

    def validate (self, name, x):
        if x <= self._value:
            raise AaValueError ("> %s" % self._value,
                                "%d (<= %d)" % (x, self._value))
        pass

    def getConditionStr (self):
        return "> %s" % self._value

    def __repr__ (self):
        return "gt(%s)" % self._value

    pass

class le (Condition):

    def __init__ (self, value):
        self._value = value
        pass

    def validate (self, name, x):
        if x > self._value:
            raise AaValueError ("<= %s" % self._value,
                                "%d (> %d)" % (x, self._value))
        pass

    def getConditionStr (self):
        return "<= %s" % self._value

    def __repr__ (self):
        return "le(%s)" % self._value

    pass

class lt (Condition):

    def __init__ (self, value):
        self._value = value
        pass

    def validate (self, name, x):
        if x >= self._value:
            raise AaValueError ("< %s" % self._value,
                                "%d (>= %d)" % (x, self._value))
        pass

    def getConditionStr (self):
        return "< %s" % self._value

    def __repr__ (self):
        return "lt(%s)" % self._value

    pass


class ofType (Condition):

    def __init__ (self, typ):
        self._type = typ
        pass

    def getTypeStr (self, typ):
        return str (typ)[7:-2]

    def validate (self, name, x):
        if type (x) is not self._type:
            raise AaValueError ("of type " + self.getTypeStr (self._type),
                                "of type " + self.getTypeStr (type (x)))
        pass

    def getConditionStr (self):
        return "of type %s" % self.getTypeStr (self._type)

    def __repr__ (self):
        return "typeOf(%s)" % self.getTypeStr (self._type)

    pass

class or_ (Condition):

    def __init__ (self, *conds):
        self._conds = list (conds)
        pass

    def validate (self, name, x):
        excs = []
        for cond in self._conds:
            try:
                cond.validate (name, x)
                break
            except AaValueError as e:
                excs.append (e)
                pass
            pass

        if len (excs) == len (self._conds):
            raise AaValueError (" or ".join (map (lambda x: "(" + x.getConditionStr () + ")", self._conds)),
                                excs[0].actual)
        pass

    def getConditionStr (self):
        return " or ".join (map (lambda x: "(" + x.getConditionStr () + ")", self._conds))

    def __repr__ (self):
        return "or(%s)" % ", ".join (map (repr, self._conds))

    pass


class not_ (Condition):

    def __init__ (self, cond):
        self._cond = cond
        pass

    def validate (self, name, x):
        result = True
        try:
            self._cond.validate (name, x)
            result = False
        except AaValueError as e:
            pass

        if result is False:
            raise AaValueError ("not (%s)" % self._cond.getConditionStr (),
                                "%s (is (%s))" % (str (x), self._cond.getConditionStr ()))
        pass

    def getConditionStr (self):
        return "not " + str (cond)

    def __repr__ (self):
        return "not(%s)" % self._cond

    pass


class ofInstance (Condition):

    def __init__ (self, ins):
        self._instance = ins
        pass

    def getClassName (self, o):
        return o.__class__.__name__ if hasattr (o, "__class__") else \
               o.__name__ if type (o) is types.ClassType else \
               "(no type)"

    def validate (self, name, x):
        if not isinstance (x, self._instance):
            raise AaValueError ("of instance %s" % self.getClassName (self._instance),
                                "%s (not of instance %s)" % (self.getClassName (x), self.getClassName (self._instance)))
        pass

    def getConditionStr (self):
        return "of instance " + self.getClassName (self._instance)

    def __repr__ (self):
        return "ofInstance(%s)" % self.getClassName (self._instance)

    pass


class iterable (Condition):

    def __init__ (self):
        pass

    def validate (self, name, x):
        if not hasattr (x, "__iter__"):
            raise AaValueError ("iterable", "%s (not iterable)" % str (x))
        pass

    def getConditionStr (self):
        return "iterable"

    def __repr__ (self):
        return "iterable()"

    pass


_callable = callable

class callable (Condition):

    def __init__ (self):
        pass

    def validate (self, name, x):
        if not _callable (x):
            raise AaValueError ("callable", "%s (not callable)" % str (x))
        pass

    def getConditionStr (self):
        return "callable"

    def __repr__ (self):
        return "callable()"

    pass


class coerce (Condition):

    def __init__ (self, typ):
        self.typ = typ
        pass

    def validate (self, name, x):
        return self.typ (x)

    def getConditionStr (self):
        return "-> %s" % self.typ

    def __repr__ (self):
        return "coerce(%s)" % self.typ

    pass


class cond (Condition):

    def __init__ (self, pred, expected):
        from ..functional import SyntheticLambda

        self._pred = SyntheticLambda._fn (pred)
        self._expected = expected
        pass

    def validate (self, name, x):
        if not self._pred (x):
            raise AaValueError (self._expected, str (x))
        pass
    
    def getConditionStr (self):
        return "cond(%s)" % self._expected

    def __repr__ (self):
        return "cond(%s)" % self._expected

    pass


class sequential (Condition, Redirectable):

    def __init__ (self):

        def _validate (name, x):
            if not hasattr (x, "__len__"):
                raise AaValueError ("sequential", "%s (not sequential)" % str (x))
            pass

        self._subconds = [_validate]
        pass

    def validate (self, name, x):
        for cond in self._subconds:
            cond (name, x)
            pass
        pass
    
    def getConditionStr (self):
        return "sequential"

    def forall (self, cond):

        def _validate (name, xs):
            for i, x in enumerate (xs):
                try:
                    cond.validate (name, x)
                except AaValueError as e:
                    s = msgs["exc.format"] % dict (name = "%s[%s]" % (name, i),
                                                   expected = "`%s[%d]' to be %s" % (name, i, e.expected % dict (name = "`%s'" % name)),
                                                   actual = e.actual % dict (name = "`%s'" % name))
                    raise ValueError (s)
                pass
            pass

        self._subconds.append (_validate)
        return self
    
    def length (self, cond):

        def _validate (name, x):
            try:
                cond.validate (name, len (x))
            except AaValueError as e:
                s = msgs["exc.format"] % dict (name = "len(%s)" % name,
                                               expected = "`len(%s)' to be %s" % (name, e.expected % dict (name = "`%s'" % name)),
                                               actual = e.actual % dict (name = "`%s'" % name))
                raise ValueError (s)
            pass

        self._subconds.append (_validate)
        return self

    def nonEmpty (self):

        def _validate (name, x):
            if len (x) == 0:
                raise AaValueError ("sequential", "%s (not sequential)" % str (x))
            pass

        self._subconds.append (_validate)
        return self

    def __repr__ (self):
        return "sequential()"

    pass


_tuple = tuple

class tuple (Condition, Redirectable):

    def __init__ (self):

        def _validate (name, x):
            if type (x) is not _tuple:
                raise AaValueError ("tuple", "%s (not tuple)" % str (x))
            pass

        self._subconds = [_validate]
        pass

    def validate (self, name, x):
        for cond in self._subconds:
            cond (name, x)
            pass
        pass

    def elem (self, n, cond):

        def _validate (name, x):
            try:
                cond.validate (name, x[n])
            except AaValueError as e:
                s = msgs["exc.format"] % dict (name = "%s[%d]" % (name, n),
                                               expected = "`%s[%d]' to be %s" % (name, n, e.expected % dict (name = "`%s'" % name)),
                                               actual = e.actual % dict (name = "`%s'" % name))
                raise ValueError (s)
            pass

        self._subconds.append (_validate)
        return self

    def length (self, cond):

        def _validate (name, x):
            try:
                cond.validate (name, len (x))
            except AaValueError as e:
                s = msgs["exc.format"] % dict (name = "len(%s)" % name,
                                               expected = "`len(%s)' to be %s" % (name, e.expected % dict (name = "`%s'" % name)),
                                               actual = e.actual % dict (name = "`%s'" % name))
                raise ValueError (s)
            pass

        self._subconds.append (_validate)
        return self

    def getConditionStr (self):
        return "tuple"

    def __repr__ (self):
        return "tuple()"

    pass
