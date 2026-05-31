import os

from bauh import __app_name__, __version__

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

__all__ = ["__app_name__", "__version__", "ROOT_DIR"]
