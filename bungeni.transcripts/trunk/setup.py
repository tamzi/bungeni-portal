from setuptools import setup, find_packages
import os

version = "0.1"

setup(name="bungeni.transcripts",
    version=version,
    author='Bungeni Developers',
    author_email="bungeni-dev@googlegroups.com",
    description="Transctipts functionality for Bungeni",
    long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
    keywords="bungeni zope3",
    # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python",
    ],
    packages=find_packages(),
    namespace_packages=["bungeni"],
    url="www.bungeni.org/",
    license="GPL",
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        # -*- Extra requirements: -*-
    ],
    entry_points="""
# -*- Entry points: -*-
""",
)

