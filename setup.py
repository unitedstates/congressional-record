from setuptools import setup

setup(name='congressional_record',
      version='0.1',
      description='Parses the U.S. Congressional Record from FDsys.',
      url='https://github.com/unitedstates/congressional-record',
      author='',
      author_email='flyingcircus@example.com',
      license='BSD3',
      packages=['congressional_record'],
      install_requires=[
            ipython==1.1.0
            lxml==3.3.0beta5
            wsgiref==0.1.2
      ],
      zip_safe=False)