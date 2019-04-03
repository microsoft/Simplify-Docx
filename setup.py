"""
Package installation via setup()
"""
import codecs
import os
import re
from setuptools import setup

#Allow single version in source file to be used here
#From https://packaging.python.org/guides/single-sourcing-package-version/
def read(*parts):
    # intentionally *not* adding an encoding option to open
    # see here: https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    here = os.path.abspath(os.path.dirname(__file__))
    return codecs.open(os.path.join(here, *parts), 'r').read()
def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(name="simplify-docx",
        version=find_version('simplify_docx', '__init__.py'),
        description="A utility for simplifying python-docx document objects",
        author="Microsoft Research",
        packages=['simplify_docx'],
        license='UNLICENSED',
        install_requires=["python-docx"])
