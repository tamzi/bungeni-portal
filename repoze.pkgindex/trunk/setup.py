import os
import sys

from ez_setup import use_setuptools
use_setuptools()

import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

requires = [
    'setuptools',
    'repoze.bfg',
    'zope.security',	
    ]
    
if sys.version_info[:3] < (2,5,1):
    print "Please upgrade to Python 2.5.1 or higher."
    sys.exit(1)    

setup(name='repoze.pkgindex',
      version=0.1,
      description='Provide an HTTP front-end for an index of custom libraries. ',
      long_description=read("README.txt"),      
      classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      keywords='file server wsgi zope',
      author="Millie Ngoka",
      author_email="repoze-dev@lists.repoze.org",
      url="http://www.repoze.org",
      license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
      packages=find_packages(),
      include_package_data=True,
      namespace_packages=['repoze'],
      zip_safe=False,
      tests_require = requires,
      install_requires = requires,
      test_suite="repoze.pkgindex.tests",
      entry_points = """\
      [paste.app_factory]
      make_app = repoze.pkgindex.run:make_app
      """,
      )

