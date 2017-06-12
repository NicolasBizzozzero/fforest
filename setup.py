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
import ensemble_experimentation.src.getters.get_global_variable as ggv

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as file:
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
            ggv.main_entry_point() + ' = ensemble_experimentation.main:main_entry_point',
            ggv.forest_entry_point() + ' = ensemble_experimentation.main:forest_entry_point',
            ggv.forest_reduction_entry_point() + ' = ensemble_experimentation.main:forest_reduction_entry_point',
        ],
    },
)
