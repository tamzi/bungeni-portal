from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='bungeni.transcripts',
      version=version,
      description="Transctipts functionality for Bungeni",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='Bungeni Zope3',
      author='Miano Njoka',
      author_email='miano@parliaments.info',
      url='www.bungeni.org/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['bungeni'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
