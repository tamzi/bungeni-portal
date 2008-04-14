from setuptools import setup, find_packages

setup(
    name="bungeni.core",
    version="0.2",
    author='Bungeni Developers',
    author_email='bungeni-dev@googlegroups.com',
    description='Data Models, Domain Classes, for Bungeni',
    keywords = "zope3 bungeni",
      classifiers = [
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'Programming Language :: Python',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: Zope3'],    
    packages=find_packages(),
    package_data = { '': ['*.txt', '*.zcml'] },
    namespace_packages=['bungeni'],
    install_requires = [ 'setuptools',
                         'SQLAlchemy',
                         'zope.schema',
                         'zope.interface',
                         'zope.i18n',
                         'ore.alchemist'],
    zip_safe = False,
    )

