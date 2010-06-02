from setuptools import setup, find_packages

setup(name='bungeni.main',
      version='0.2',
      description="server packaging, deployment, startup of bungeni server",
      long_description="",
      keywords='',
      author='Bungeni Developers',
      author_email='bungeni-dev@googlegroups.com',
      url='http://www.bungeni.org',
      license='GPL',
      # Get more from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Programming Language :: Python',
                   'Environment :: Web Environment',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
                   'Framework :: Zope3',
                   ],

      packages=find_packages(),
      namespace_packages=['bungeni'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
			# Following packages are required by :
			# bungeni.server
                        'ZODB3',
                        'ZConfig',
                        'zdaemon',
                        'zope.publisher',
                        'zope.traversing',
                        'zope.app.wsgi>=3.4.0',
                        'zope.app.appsetup',
                        'zope.app.zcmlfiles',
                        # The following packages aren't needed from the
                        # beginning, but end up being used in most apps
                        'zope.annotation',
                        'zope.copypastemove',
                        'zope.formlib',
                        'zope.i18n',
                        'zope.app.authentication',
                        'zope.app.session',
                        'zope.app.intid',
                        'zope.app.keyreference',
                        'zope.app.catalog',
                        # The following packages are needed for functional
                        # tests only
                        'zope.testing',
                        'zope.app.testing',
                        'zope.app.securitypolicy',
                        'zope.sendmail',
                        'ore.wsgiapp',
			#
			# The following are required by bungeni.models	
                        'SQLAlchemy',
                        'zope.schema',
                        'zope.interface',
                        'zope.i18n',
                        'alchemist.catalyst',
                        'alchemist.security',
                        'ore.alchemist',
                        # The following are required by bungeni.portal
			#
		        'pyquery>=0.3.1',
		        'Deliverance',
		        'chameleon.html',
			# The following are used by bungeni.core 
			#
                        'ore.xapian',
                        'ore.workflow',
                        'z3c.dav',
                        'plone.i18n',
                        'plone.transforms',
			# The followning are used by bungeni.ui
                        'simplejson',
                        'zope.app.cache',
                        'plone.memoize',
                        'alchemist.ui',
                        'marginalia',
                        'ore.yui',
                        'z3c.menu.ready2go',			
                        'zc.displayname',
                        'zope.formlib',
			],
      entry_points =  """
	      [paste.app_factory]
	      main = bungeni.server.startup:application_factory

	      [paste.filter_app_factory]
	      deliverance = bungeni.portal.middleware:make_deliverance_middleware

	      [paste.app_factory]
	      static = bungeni.portal.app:make_static_serving_app
	      """,
	      {
	        'console_scripts':[
	            'bungeni-reset-db = bungeni.core.schema:reset_database',
        	    'bungeni-sync-index = bungeni.core.index:reset_index',
	            ]
              },
      )




from setuptools import setup, find_packages

setup(
    name="bungeni.ui",
    version="0.2",
    author='Bungeni Developers',
    author_email='bungeni-dev@googlegroups.com',
    description='UI for Bungeni, based on Plone',
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
    namespace_packages=['bungeni'],
    install_requires = [ 'setuptools',
                         'bungeni.core',
                         'bungeni.models',
                         'simplejson',
                         'zope.app.cache',
                         'plone.memoize',
                         'alchemist.ui',
                         'marginalia',
                         'ore.yui',
                         'z3c.menu.ready2go',			
                         'zc.displayname',
                         'zope.formlib'],
    zip_safe = False,
    )

