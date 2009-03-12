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
                         'Amara',
                         'SQLAlchemy',
                         'zope.schema',
                         'zope.interface',
                         'zope.i18n',
                         'alchemist.catalyst',
                         'alchemist.security',
                         'ore.wsgiapp',
                         'ore.xapian',
                         'ore.alchemist',
                         'ore.workflow',
                         'bungeni.models',
                         'z3c.dav'],
    entry_points={
        'console_scripts':[
            'bungeni-reset-db = bungeni.core.schema:reset_database',
            'bungeni-sync-index = bungeni.core.index:reset_index',
            ]
        },    
    zip_safe = False,
    )

