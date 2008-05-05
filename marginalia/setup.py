from setuptools import setup, find_packages

setup(
    name="marginalia",
    version="0.2",
    author='Bungeni Developers',
    author_email='bungeni-dev@googlegroups.com',
    description='Marginalia user document annotations',
    license="GPL",
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
    package_data = { '': ['*.txt', '*.zcml', '*.pt'] },
    install_requires = [ 'setuptools',
                         'bungeni.core',
                         'zope.formlib'],
    zip_safe = False,
    )

