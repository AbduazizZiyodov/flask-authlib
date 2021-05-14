import pathlib

from setuptools import setup
from setuptools import find_packages

from flask_authlib import (
    __author__, __author_email__, __copyright__, __copyright__,
    __description__, __license__, __title__, __url__, __version__
)


setup(
    name=__title__,
    version=__version__,
    license=__license__,
    author=__author__,
    author_email=__author_email__,
    url=__url__,
    description=__description__,
    platforms='any',
    packages=find_packages(),
    copyright=__copyright__,
    install_requires=["flask", "flask_login", "psycopg2-binary",
                      "sqlalchemy", "flask_sqlalchemy", "flask_bcrypt"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        'Programming Language :: Python :: Implementation :: CPython',
        'Environment :: Web Environment'
    ]
)
