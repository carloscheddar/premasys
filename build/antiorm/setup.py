#!/usr/bin/env python

"""
Install script for the Anti-ORM library.
"""

__author__ = "Martin Blais <blais@furius.ca>"

from distutils.core import setup

def read_version():
    try:
        return open('VERSION', 'r').readline().strip()
    except IOError, e:
        raise SystemExit(
            "Error: you must run setup from the root directory (%s)" % str(e))


# Include all files without having to create MANIFEST.in
def add_all_files(fun):
    import os, os.path
    from os.path import abspath, dirname, join
    def f(self):
        for root, dirs, files in os.walk('.'):
            if '.hg' in dirs: dirs.remove('.hg')
            self.filelist.extend(join(root[2:], fn) for fn in files
                                 if not fn.endswith('.pyc'))
        return fun(self)
    return f
from distutils.command.sdist import sdist
sdist.add_defaults = add_all_files(sdist.add_defaults)


setup(name="antiorm",
      version=read_version(),
      description=\
      "A Pythonic Helper for DBAPI-2.0 SQL Access",
      long_description="""
Anti-ORM is not an ORM, and it certainly does not want to be.  Anti-ORM is a
simple Python module that provides a pythonic syntax for making it more
convenient to build SQL queries over the DBAPI-2.0 interface.

In practice, if you're the kind of person that likes it to the bare metal, it's
almost as good as the ORMs.  At least there is no magic, and it just works.
""",
      license="GPL",
      author="Martin Blais",
      author_email="blais@furius.ca",
      url="http://furius.ca/antiorm",
      package_dir = {'': 'lib/python'},
      py_modules = ('antiorm', 'dbapiext', 'antipool', 'dbrelmgr'),
      ## data_files=[('Poodle', ['VERSION'])],
     )

