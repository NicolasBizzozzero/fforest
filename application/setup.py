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

import ensemble_experimentation

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='processus_apprentissage',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=ensemble_experimentation.__version__,

    description='Graphical tool to convert a number from one base to another',
    long_description=long_description,

    # The project's main homepage.
    # TODO: Replace
    url='',

    # Not to use with Python versions prior to 2.2.3 or 2.3
    # TODO: Replace
    download_url='',

    # Author details
    author=ensemble_experimentation.__author__,
    author_email='nicolasbizzozzero@gmail.com',

    # Choose your license
    license='GPL-3.0',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        "Natural Language :: French",
        'Intended Audience :: Science/Research',
        "Topic :: Scientific/Engineering :: Artificial Intelligence",

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords='Command-line tools to split and play with Fuzzy Forests.',

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
    install_requires=["docopt >= 0.6.2"],

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
            'ensemble_experimentation = ensemble_experimentation.main:main_ensemble_experimentation',
            'ensemble_foret_classique = ensemble_experimentation.main:main_ensemble_foret_classique',
            'ensemble_foret_reduction = ensemble_experimentation.main:main_ensemble_foret_reduction',
        ],
    },
)
