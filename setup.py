
from setuptools import setup, find_packages

setup(
    name = 'tesql',
    version = '0.0.0',
    packages = find_packages(exclude=['tests', 'tests.*']),

    author = 'Yuri Vasilevski',
    author_email = 'yvasilev@gentoo.org',
    description = 'Text based SQL like backend with nice object oriented '
                  'interface (ORM)',
    license = 'GPL-3',
    keywords = 'SQL ORM database',
    url = 'http://github.com/yvasilev/resql',

    setup_requires=[
        'nose>=0.11',
    ],

    test_suite = 'nose.collector',
)
