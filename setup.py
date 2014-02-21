from setuptools import setup, find_packages

setup(
    name='congressionalrecord',
    version='0.1',
    description='Parses the U.S. Congressional Record from FDsys.',
    url='https://github.com/unitedstates/congressional-record',
    author='Lindsay Young',
    author_email='lyoung@sunlightfoundation.com',
    license='BSD3',
    packages=find_packages(),
    install_requires=[
        'lxml==3.3.0beta5',
    ],
    entry_points={
        'console_scripts': ['parsecr = congressionalrecord.cli:main']},
    zip_safe=False
)
