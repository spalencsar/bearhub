import os

try:
    from bauh import __app_name__, __version__
except ModuleNotFoundError:
    __app_name__ = "bearhub"
    __version__ = "0.10.7"

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

__all__ = ["__app_name__", "__version__", "ROOT_DIR"]
