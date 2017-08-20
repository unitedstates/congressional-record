from setuptools import setup, find_packages

setup(
    name='congressionalrecord2',
    version='0.9.1',
    description='Parse the U.S. Congressional Record from FDsys.',
    url='https://github.com/nclarkjudd/congressionalrecord2',
    author='Nick Judd',
    author_email='nick@nclarkjudd.com',
    license='BSD3',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4 >= 4.4.0',
        'lxml >= 3.3.5',
        'numpy >= 1.9.0',
        'psycopg2 >= 2.6.1',
        'pyelasticsearch >= 1.4',
        'SQLAlchemy >= 1.0.8',
        'requests >= 2.7.0',
        'PyYAML >= 3.11',
        ],
        zip_safe=False
    )
