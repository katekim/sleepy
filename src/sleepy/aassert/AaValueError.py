import os, yaml

msgs = yaml.safe_load (open (os.path.join (os.path.dirname (__file__), "messages.yaml")).read ())

class AaValueError:

    def __init__ (self, expected, actual):
        self.expected = expected
        self.actual = actual
        pass

    pass

