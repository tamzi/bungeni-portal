from setuptools import setup, find_packages

setup(
    name="appy",
    version="0.0.1",
    description='Programatic Document creation',
    packages=find_packages(),
    package_data = { 'appy.pod':['test/*']},
    install_requires = [ 'setuptools'],
    zip_safe = False,
    )
