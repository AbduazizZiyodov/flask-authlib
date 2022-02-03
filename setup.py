from os import path

from setuptools import setup
from setuptools import find_packages

parent_dir: str = path.abspath(path.dirname(__file__))
readme_file: str = path.join(parent_dir, "README.md")

with open(readme_file, encoding="utf-8") as f:
    long_description: str = f.read()


setup(
    license='MIT',
    name='Flask-Authlib',
    author='Abduaziz Ziyodov',
    version='1.5.0',

    long_description=long_description,
    long_description_content_type="text/markdown",

    author_email='abduaziz.ziyodov@mail.ru',
    url='https://github.com/AbduazizZiyodov/flask-authlib',
    description='Authentication library for Flask Web Framework ',

    install_requires=[
        "flask", "flask_login",
        "sqlalchemy", "flask_sqlalchemy", "flask_bcrypt",
        "cryptography==3.3.2", "python-jose", "jwt",
        "pydantic", "email-validator", "rich"
    ],

    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Environment :: Web Environment"
    ],

    platforms="any",
    include_package_data=True,
    packages=find_packages(),
    package_data={
        "flask_authlib": ["templates.zip", "database", "jwt"]
    }
)
