def extract(g={}):
    from sleepy import aassert, collection, functional

    g['List'] = collection.List
    g['MList'] = collection.MList
    g['Nil'] = collection.Nil
    g['Seq'] = collection.Seq
    g['Map'] = collection.Map
    g['MMap'] = collection.MMap

    g['It'] = collection.IterableOnce
    g['L'] = collection.List
    g['ML'] = collection.MList
    g['Li'] = collection.List.fromIterator
    g['MLi'] = collection.MList.fromIterator
    g['M'] = collection.Map
    g['MM'] = collection.MMap
    g['Md'] = collection.Map.fromDict
    g['MMd'] = collection.MMap.fromDict
    g['Mi'] = collection.Map.fromIterator
    g['MMi'] = collection.MMap.fromIterator

    g['Just'] = collection.Just
    g['Nothing'] = collection.Nothing

    g['SL'] = functional.SyntheticLambda
    g['_'] = functional.Recorder0()
    g['Val'] = functional.Val
    g['Match'] = functional.Match
    g['F'] = functional.SyntheticLambda.fn
    for i in range(0, 10):
        g['F%d' % i] = functional.SyntheticLambda.fn(i)

    g['tail_call'] = functional.tail_call

    g['aa'] = aassert.Decorator()

    def p(*args, **kwargs):
        import sys

        sep = kwargs.get('sep', ' ')
        file = kwargs.get('file', sys.stdout)
        end = kwargs.get('end', '\n')
        file.write(sep.join(map(str, args)) + end)

    g['P'] = p

    return g


g = extract()
for k, v in g.items():
    locals()[k] = v

__all__ = g.keys()
