import pathlib
from setuptools import setup, find_packages

from flask_authlib import __version__


BASE_PATH = pathlib.Path(__file__).parent

README = (BASE_PATH / "README.md").read_text()


setup(
    name="flask-authlib",
    version=__version__,
    license="MIT",
    author="Abduaziz Ziyodov",
    author_email="abduaziz.ziyodov@mail.ru",
    url="https://github.com/AbduazizZiyodov/flask-authlib",
    long_description=README,
    long_description_content_type="text/markdown",
    description="Authentication library for Flask Web Framework ",
    platforms='any',
    packages=find_packages(),
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
