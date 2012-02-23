from Iterable import IterableOnce, Iterable
from List import List, MList
from Map import Map, MapLike, MMap, MMapLike
from Maybe import Just, Nothing
from Seq import Seq
from Sequential import MSequential, Sequential
from Set import Set

Nil = List ()

try:
    import yaml

    for t in (IterableOnce, List, MList, Seq):
        yaml.add_representer(
            t, lambda d, x: d.represent_data(x.toBuiltinList()))

    for t in (Map, MMap):
        yaml.add_representer(
            t, lambda d, x: d.represent_data(x.toBuiltinMap()))
except ImportError:
    pass
