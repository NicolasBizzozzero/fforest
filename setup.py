"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
import fforest.src.getters.get_global_variable as ggv


# TODO: Implement one entry-point for each phase :
"""
    entry_points={
        'console_scripts': [
            ggv.main_entry_point() + ' = fforest.main:main_entry_point',
            ggv.preprocessing_entry_point() + ' = fforest.main:preprocessing_entry_point',
            ggv.initial_split_entry_point() + ' = fforest.main:initial_split_entry_point',
            ggv.reference_split_entry_point() + ' = fforest.main:reference_split_entry_point',
            ggv.subsubtrain_split_entry_point() + ' = fforest.main:subsubtrain_split_entry_point',
            ggv.learning_entry_point() + ' = fforest.main:learning_entry_point',
            ggv.reduction_entry_point() + ' = fforest.main:reduction_entry_point',
            ggv.quality_entry_point() + ' = fforest.main:quality_entry_point',
            ggv.classes_matrices_entry_point() + ' = fforest.main:classes_matrices_entry_point',
        ],
    },
"""


_HERE = path.abspath(path.dirname(__file__))
_README_FILE_NAME = "README.md"
_README_FILE_ENCODING = "utf8"


# Get the long description from the README file
with open(path.join(_HERE, _README_FILE_NAME), encoding=_README_FILE_ENCODING) as file:
    long_description = file.read()

setup(
    name=ggv.name(),

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=ggv.version(),

    description=ggv.description(),
    long_description=long_description,

    # The project's main homepage.
    url=ggv.main_homepage(),

    # Not to use with Python versions prior to 2.2.3 or 2.3
    download_url=ggv.download_url(),

    # Author details
    author=ggv.author(),
    author_email=ggv.email(),

    # Choose your license
    license=ggv.license_used(),

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=ggv.classifiers(),

    # What does your project relate to?
    keywords=ggv.keywords(),

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=ggv.dependencies(),

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={

    },

    # Set to True if we use MANIFEST.in
    include_package_data=True,

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            ggv.main_entry_point() + ' = fforest.main:main_entry_point',
        ],
    },
)
