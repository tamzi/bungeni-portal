from setuptools import setup, find_packages

setup(
    name="ploned.ui",
    version="0.2",
    author='Kapil Thangavelu',
    author_email='kapil.foss@gmail.com',
    description='Plone Skin for Zope 3 Applications',
    license="GPL",
    keywords = "zope3",
    classifiers = [
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'Programming Language :: Python',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: Zope3'],
    packages=find_packages(),
    package_data = { '': ['*.txt', '*.zcml', '*.pt', '*.css', '*.gif', '*.png'] },
    namespace_packages=['ploned'],
    install_requires = [ 'setuptools',
                         'zope.publisher',
                         'zope.documenttemplate',
                         'zope.viewlet'],
    zip_safe = False,
    )

