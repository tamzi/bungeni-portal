from setuptools import setup, find_packages

setup(
    name="bungeni.messaging",
    version="0.1",
    author='Bungeni Developers',
    author_email='bungeni-dev@googlegroups.com',
    description='Messaging capabilities for Bungeni',
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
                         'zope.schema',
                         'zope.interface',
                         'zope.sendmail', ],
    zip_safe = False,
    )

