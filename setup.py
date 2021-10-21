from os import path

from setuptools import setup
from setuptools import find_packages

from flask_authlib.info import About


parent_dir: str = path.abspath(path.dirname(__file__))
readme_file: str = path.join(parent_dir, "README.md")

with open(readme_file, encoding="utf-8") as f:
    long_description: str = f.read()

setup(
    name=About.name,
    version=About.version,
    license=About.license,
    author=About.author,
    author_email=About.author_email,
    url=About.url,
    description=About.description,
    platforms="any",
    include_package_data=True,
    packages=find_packages(),
    copyright=About.copyright,
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=About.requires,
    classifiers=About.classifiers
)
