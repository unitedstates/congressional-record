from setuptools import setup, find_packages
from congressionalrecord import __version__

setup(
    name='congressionalrecord',
    version=__version__,
    description='Parse the U.S. Congressional Record from FDsys.',
    url='https://github.com/unitedstates/congressional-record',
    author='Lindsay Young',
    author_email='lyoung@sunlightfoundation.com',
    license='BSD3',
    packages=find_packages(),
    install_requires=[
        'lxml==3.3.5',
    ],
    entry_points={
        'console_scripts': ['parsecr = congressionalrecord.cli:main']},
    zip_safe=False
)
