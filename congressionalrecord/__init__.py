import pkg_resources  # part of setuptools
VERSION = pkg_resources.require("congressionalrecord")[0].version

__version__ = VERSION
