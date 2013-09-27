import marshal

try:
    import cPickle as pickle
except ImportError:
    import pickle


class Graph(dict):

    """A very simple graph type.

    Its structure looks like this::

        {u: {v: e, ...}, ...}  # Node v is a adjacent to u via edge e

    Edges can be of any type. Nodes have to be hashable since they're
    used as dictionary keys.

    """

    def __init__(self, data=None):
        if data:
            self.update(data)

    def add_edge(self, u, v, edge=None):
        """Add an ``edge`` from ``u`` to ``v``."""
        self.setdefault(u, {})
        self[u][v] = edge

    def add_node(self, u, neighbors=None):
        """Add the node ``u``.

        ``neighbors``
            An optional dict of nodes adjacent to ``u`` and the edges
            that connect them: {v: edge, ...}. An edge will be added
            from ``u`` to each ``v`` in ``neighbors``.

        """
        self.setdefault(u, {})
        if neighbors:
            for v, edge in neighbors.items():
                self[u][v] = edge

    @classmethod
    def load(cls, path):
        """Load pickled `Graph` from ``path``."""
        with open(path, 'rb') as loadfile:
            return pickle.load(loadfile)

    def dump(self, path):
        """Dump pickled graph to ``path``."""
        with open(path, 'wb') as dumpfile:
            pickle.dump(self, dumpfile)

    @classmethod
    def unmarshal(cls, path):
        """Read graph from disk using marshal.

        Marshalling is quite a bit faster than pickling, but only the
        following types are supported: booleans, integers, long
        integers, floating point numbers, complex numbers, strings,
        Unicode objects, tuples, lists, sets, frozensets, dictionaries,
        and code objects.

        The method names `unmarshal` and `marshal` were chosen based on
        this note in the standard library documentation: "Strictly
        speaking, 'to marshal' means to convert some data from internal
        to external form and 'unmarshalling' for the reverse process."

        """
        with open(path, 'rb') as loadfile:
            data = marshal.load(loadfile)
        return Graph(data)

    def marshal(self, path):
        """Write graph to disk using marshal.

        See note in :meth:`unmarshal`.

        """
        with open(path, 'wb') as dumpfile:
            marshal.dump(dict(self), dumpfile)
