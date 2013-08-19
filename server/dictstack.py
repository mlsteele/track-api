class DictStack(object):
    """
    A stack of dictionaries.

    Dictionaries further down the stack will override top-level values from
    prior dictionaries.
    """
    def __init__(self, first_dict=None):
        self.stack = []
        if first_dict is not None:
            self.push(first_dict)

    def push(self, d):
        self.stack.append(d)

    def pop(self):
        self.stack.pop()

    def get_dict(self):
        """ Get the visible dictionary with overridden values not visible. """
        out = {}
        for d in self.stack:
            out.update(d)

        return out

    def __str__(self):
        return str(self.get_dict())

    def __iter__(self):
        return self.get_dict().iteritems()


if __name__ == '__main__':
    print "testing..."
    ds = DictStack()
    print ds.get_dict()
    ds.push({'a': 'b', 'c': 'd', 'e': {'f': 'g'}})
    print ds
    ds.push({'c': 'OVERRIDE'})
    print ds
    ds.push({'e': {'override': 'stuff'}})
    print ds
    ds.pop()
    print ds
    ds.pop()
    print ds
    print dict(ds)
