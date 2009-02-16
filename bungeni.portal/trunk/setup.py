from setuptools import setup, find_packages

setup(
    name="bungeni.portal",
    version="0.1",
    author='Bungeni Developers',
    author_email='bungeni-dev@googlegroups.com',
    description="Portal integration using Deliverance.",
    keywords = "zope3 bungeni deliverance",
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
    install_requires = [
        'Deliverance',
        'ore.alchemist',
        'bungeni.models',
        'alchemist.security',
        'chameleon.html',
        ],
    entry_points = """\
    [paste.filter_app_factory]
    deliverance = bungeni.portal.middleware:make_deliverance_middleware

    [paste.app_factory]
    static = bungeni.portal.app:make_static_serving_app

    """,
    zip_safe = False,
    )

