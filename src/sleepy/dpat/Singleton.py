from __future__ import with_statement
import threading

class Singleton:

    __lock = threading.Lock ()
    __instance = None

    @classmethod
    def getInstance (cls):
        with cls.__lock:
            if cls.__instance is None:
                cls.__instance = cls ()
                pass

            instance = cls.__instance
            pass

        return instance

    pass
