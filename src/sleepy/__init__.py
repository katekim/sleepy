version = "0.0.1"

from Extensible import Extensible

import aassert
import collection
import extract
import dpat
import functional

def _debug (*args):
    import os, sys

    if os.getenv ("DEBUG") is not None:
        print >>sys.stderr, "[DEBUG] %s" % " ".join (map (str, args))
        pass
    pass
