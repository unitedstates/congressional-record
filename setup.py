from setuptools import setup, find_packages

setup(
    name='congressionalrecord',
    version='2.0.1',
    description='Parse the U.S. Congressional Record from GovInfo.',
    url='https://github.com/unitedstates/congressional-record',
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
        'requests[security]',
        'PyYAML >= 3.11',
        'unicodecsv',
        'future'
        ],
        zip_safe=False
    )
