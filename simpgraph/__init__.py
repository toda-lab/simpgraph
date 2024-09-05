# simpgraph: Simple Python module for unordered graphs

import importlib.metadata

__version__ = importlib.metadata.version(__package__)

from .simpgraph import SimpGraph

__all__ = [
    "SimpGraph",
]
